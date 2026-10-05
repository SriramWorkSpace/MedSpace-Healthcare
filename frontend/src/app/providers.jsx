import { QueryClientProvider } from "@tanstack/react-query";
import { MotionConfig } from "motion/react";
import { Toaster } from "sonner";
import { queryClient } from "@/lib/queryClient";
import { AuthProvider } from "@/lib/auth";
import { ThemeProvider, useTheme } from "@/lib/theme";
import { EasterEggProvider } from "@/easter-eggs/EasterEggs";

function ThemedToaster() {
  const { resolved } = useTheme();
  return (
    <Toaster
      theme={resolved}
      position="bottom-right"
      closeButton
      toastOptions={{
        style: {
          fontFamily: "var(--font-sans)",
          borderRadius: "14px",
          border: "1px solid var(--line)",
          background: "var(--surface)",
          color: "var(--ink)",
          boxShadow: "var(--shadow-md)",
        },
      }}
    />
  );
}

export function Providers({ children }) {
  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <MotionConfig reducedMotion="user">
            <EasterEggProvider>
              {/* Before the pages, so it listens before any page's first effect fires a toast. */}
              <ThemedToaster />
              {children}
            </EasterEggProvider>
          </MotionConfig>
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}
