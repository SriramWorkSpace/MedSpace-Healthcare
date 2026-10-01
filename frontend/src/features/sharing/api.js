import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const shareKeys = { all: ["shares"] };

export function useShares() {
  return useQuery({ queryKey: shareKeys.all, queryFn: () => api.get("/api/shares") });
}

export function useCreateShare() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body) => api.post("/api/shares", body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: shareKeys.all });
      qc.invalidateQueries({ queryKey: ["audit"] });
    },
  });
}

export function useRevokeShare() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => api.delete(`/api/shares/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: shareKeys.all });
      qc.invalidateQueries({ queryKey: ["audit"] });
    },
  });
}

export function usePublicShare(token) {
  return useQuery({
    queryKey: ["public-share", token],
    queryFn: () => api.get(`/api/public/shares/${token}`),
    retry: false,
    staleTime: Infinity, // every fetch counts as a view
  });
}

export const publicPreviewUrl = (token, docId, page = 1) =>
  `/api/public/shares/${token}/documents/${docId}/pages/${page}/preview`;
export const publicFileUrl = (token, docId) =>
  `/api/public/shares/${token}/documents/${docId}/file`;
