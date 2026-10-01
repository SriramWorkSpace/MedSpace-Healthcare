import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, ApiError, readCookie } from "@/lib/api";

export const askKeys = {
  threads: ["assistant", "threads"],
  thread: (id) => ["assistant", "thread", id],
};

export function useThreads() {
  return useQuery({ queryKey: askKeys.threads, queryFn: () => api.get("/api/assistant/threads") });
}

export function useThread(id) {
  return useQuery({
    queryKey: askKeys.thread(id),
    queryFn: () => api.get(`/api/assistant/threads/${id}`),
    enabled: Boolean(id),
  });
}

export function useCreateThread() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.post("/api/assistant/threads", {}),
    onSuccess: () => qc.invalidateQueries({ queryKey: askKeys.threads }),
  });
}

export function useDeleteThread() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.delete(`/api/assistant/threads/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: askKeys.threads }),
  });
}

/**
 * POST a question and consume the server-sent event stream.
 * EventSource can't POST or send the CSRF header, so this parses SSE frames from fetch().
 */
export async function streamAnswer(threadId, content, { onSources, onToken, onDone, onError, signal }) {
  const res = await fetch(`/api/assistant/threads/${threadId}/messages`, {
    method: "POST",
    credentials: "include",
    signal,
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
      "X-CSRF-Token": readCookie("ms_csrf") ?? "",
    },
    body: JSON.stringify({ content }),
  });
  if (!res.ok || !res.body) {
    const problem = await res.json().catch(() => ({ detail: "The assistant is unavailable." }));
    throw new ApiError(res.status, problem);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let sep;
    while ((sep = buffer.indexOf("\n\n")) !== -1) {
      const frame = buffer.slice(0, sep);
      buffer = buffer.slice(sep + 2);
      let event = "message";
      let data = "";
      for (const line of frame.split("\n")) {
        if (line.startsWith("event: ")) event = line.slice(7);
        else if (line.startsWith("data: ")) data += line.slice(6);
      }
      const payload = data ? JSON.parse(data) : {};
      if (event === "sources") onSources?.(payload);
      else if (event === "token") onToken?.(payload.t);
      else if (event === "done") onDone?.(payload);
      else if (event === "error") onError?.(payload);
    }
  }
}
