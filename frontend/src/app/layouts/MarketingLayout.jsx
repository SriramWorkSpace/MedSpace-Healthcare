import { Outlet } from "react-router";
import { MarketingNav } from "@/features/marketing/MarketingNav";
import { Footer } from "@/features/marketing/Footer";

export default function MarketingLayout() {
  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-3 focus:z-[100] focus:rounded-lg focus:bg-surface focus:px-3 focus:py-2"
      >
        Skip to content
      </a>
      <MarketingNav />
      <main id="main">
        <Outlet />
      </main>
      <Footer />
    </>
  );
}
