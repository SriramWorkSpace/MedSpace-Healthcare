import { QueryClient } from "@tanstack/react-query";
import { ApiError } from "./api";
import { doseRequest } from "@/features/doses/request";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
      retry: (count, error) => {
        if (error instanceof ApiError && error.status < 500) return false;
        return count < 2;
      },
    },
    mutations: { retry: false },
  },
});

// Dose ticks made offline pause, persist and resume with this function (ADR-025).
queryClient.setMutationDefaults(["dose"], { mutationFn: doseRequest });
