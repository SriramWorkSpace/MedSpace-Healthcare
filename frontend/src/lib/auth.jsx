import { createContext, useCallback, useContext, useEffect, useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, readCookie, refreshSession, setSessionExpiredHandler } from "./api";
import { clearOfflineCopy } from "./offline";
import { setActing } from "./acting";

const AuthContext = createContext(null);
export const meKey = ["auth", "me"];

async function fetchMe() {
  const { user } = await api.get("/api/auth/session");
  if (user) return user;
  // Access token expired but a session may still be refreshable.
  if (readCookie("ms_csrf") && (await refreshSession())) {
    return (await api.get("/api/auth/session")).user;
  }
  return null;
}

export function AuthProvider({ children }) {
  const qc = useQueryClient();
  const me = useQuery({ queryKey: meKey, queryFn: fetchMe, staleTime: 5 * 60_000 });

  const setSession = useCallback(
    (session) => {
      qc.setQueryData(meKey, session?.user ?? null);
    },
    [qc],
  );

  useEffect(() => {
    setSessionExpiredHandler(() => {
      clearOfflineCopy();
      qc.setQueryData(meKey, null);
    });
  }, [qc]);

  const logout = useMutation({
    mutationFn: () => api.post("/api/auth/logout"),
    onSettled: () => {
      clearOfflineCopy();
      setActing(null);
      qc.clear();
      qc.setQueryData(meKey, null);
    },
  });

  const value = useMemo(
    () => ({
      user: me.data ?? null,
      isLoading: me.isPending,
      setSession,
      logout: logout.mutateAsync,
      refetch: me.refetch,
    }),
    [me.data, me.isPending, me.refetch, setSession, logout.mutateAsync],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
