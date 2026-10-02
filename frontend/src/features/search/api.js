import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useSearch(q) {
  const query = q.trim();
  return useQuery({
    queryKey: ["search", query],
    queryFn: ({ signal }) => api.get(`/api/search?q=${encodeURIComponent(query)}`, { signal }),
    enabled: query.length >= 2,
    placeholderData: keepPreviousData,
    staleTime: 15_000,
  });
}
