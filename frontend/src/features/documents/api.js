import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, ApiError, readCookie } from "@/lib/api";

export const docKeys = {
  all: ["documents"],
  list: (filters) => ["documents", "list", filters ?? {}],
  detail: (id) => ["documents", "detail", id],
  extraction: (id) => ["documents", "extraction", id],
  evidence: (id) => ["documents", "evidence", id],
};

const ACTIVE = new Set(["queued", "processing"]);
export const isProcessing = (status) => ACTIVE.has(status);

export function useDocuments(filters) {
  return useQuery({
    queryKey: docKeys.list(filters),
    queryFn: () => {
      const qs = new URLSearchParams(Object.entries(filters ?? {}).filter(([, v]) => v));
      return api.get(`/api/documents${qs.size ? `?${qs}` : ""}`);
    },
    refetchInterval: (q) =>
      q.state.data?.items?.some((d) => isProcessing(d.status)) ? 1500 : false,
  });
}

export function useDocument(id) {
  return useQuery({
    queryKey: docKeys.detail(id),
    queryFn: () => api.get(`/api/documents/${id}`),
    refetchInterval: (q) => (isProcessing(q.state.data?.status) ? 1200 : false),
  });
}

export function useExtraction(id, { enabled = true } = {}) {
  return useQuery({
    queryKey: docKeys.extraction(id),
    queryFn: () => api.get(`/api/documents/${id}/extraction`),
    enabled,
    retry: false,
  });
}

/** Where each extracted field is printed on the page (ADR-031). */
export function useEvidence(id, { enabled = true } = {}) {
  return useQuery({
    queryKey: docKeys.evidence(id),
    queryFn: () => api.get(`/api/documents/${id}/evidence`),
    enabled,
    retry: false,
    staleTime: Infinity, // fixed for an extraction; reprocessing invalidates docKeys.all
  });
}

export function useDeleteDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.delete(`/api/documents/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: docKeys.all });
      qc.invalidateQueries({ queryKey: ["records"] });
    },
  });
}

export function useReprocessDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.post(`/api/documents/${id}/reprocess`),
    onSuccess: (doc) => {
      qc.setQueryData(docKeys.detail(doc.id), (old) => (old ? { ...old, ...doc } : old));
      qc.invalidateQueries({ queryKey: docKeys.all });
    },
  });
}

export function useUpdateDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...body }) => api.patch(`/api/documents/${id}`, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: docKeys.all }),
  });
}

export function useConfirmExtraction() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ extractionId, body }) =>
      api.post(`/api/extractions/${extractionId}/confirm`, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: docKeys.all });
      qc.invalidateQueries({ queryKey: ["records"] });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
      qc.invalidateQueries({ queryKey: ["timeline"] });
    },
  });
}

export function useDiscardExtraction() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (extractionId) => api.post(`/api/extractions/${extractionId}/discard`),
    onSuccess: () => qc.invalidateQueries({ queryKey: docKeys.all }),
  });
}

export const previewUrl = (docId, page = 1) => `/api/documents/${docId}/pages/${page}/preview`;
export const downloadUrl = (docId) => `/api/documents/${docId}/file`;

/**
 * Upload with progress (fetch has no upload progress events).
 * @returns {{ promise: Promise<any>, abort: () => void }}
 */
export function uploadDocument(file, { onProgress, kind } = {}) {
  const xhr = new XMLHttpRequest();
  const promise = new Promise((resolve, reject) => {
    const form = new FormData();
    form.append("file", file);
    if (kind) form.append("kind", kind);
    xhr.open("POST", "/api/documents");
    xhr.withCredentials = true;
    xhr.setRequestHeader("X-CSRF-Token", readCookie("ms_csrf") ?? "");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress?.(e.loaded / e.total);
    xhr.onload = () => {
      let body = null;
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        /* non-JSON error page */
      }
      if (xhr.status >= 200 && xhr.status < 300) resolve(body);
      else reject(new ApiError(xhr.status, body ?? { detail: "Upload failed." }));
    };
    xhr.onerror = () =>
      reject(new ApiError(0, { detail: "Network error. Check your connection." }));
    xhr.onabort = () => reject(new ApiError(0, { detail: "Upload cancelled.", code: "aborted" }));
    xhr.send(form);
  });
  return { promise, abort: () => xhr.abort() };
}
