import { Link } from "react-router";
import { GithubLogo } from "@phosphor-icons/react";
import { Logo } from "@/components/ui/Logo";

export function Footer() {
  return (
    <footer className="border-t border-line">
      <div className="mx-auto grid max-w-[1280px] gap-10 px-4 py-12 sm:px-6 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <Logo />
          <p className="mt-4 max-w-[42ch] text-sm text-ink-2">
            A portfolio project built on synthetic data. Not a medical device, not HIPAA compliant,
            and not a substitute for your care team.
          </p>
          <p className="mt-4 text-xs text-ink-3">
            Laughter is the best medicine. Still, follow your prescription.
          </p>
        </div>
        <nav aria-label="Product" className="grid content-start gap-2.5 text-sm">
          <p className="font-semibold">Product</p>
          <a href="/#how-it-works" className="text-ink-2 hover:text-ink">
            How it works
          </a>
          <a href="/#features" className="text-ink-2 hover:text-ink">
            Features
          </a>
          <a href="/#privacy" className="text-ink-2 hover:text-ink">
            Privacy
          </a>
          <Link to="/login" className="text-ink-2 hover:text-ink">
            Sign in
          </Link>
        </nav>
        <nav aria-label="Project" className="grid content-start gap-2.5 text-sm">
          <p className="font-semibold">Project</p>
          <a
            href="https://github.com/SriramWorkSpace/MedSpace-Healthcare"
            className="inline-flex items-center gap-1.5 text-ink-2 hover:text-ink"
            target="_blank"
            rel="noreferrer"
          >
            <GithubLogo size={15} /> Source code
          </a>
          <a
            href="https://github.com/SriramWorkSpace/MedSpace-Healthcare/blob/main/docs/architecture.md"
            className="text-ink-2 hover:text-ink"
            target="_blank"
            rel="noreferrer"
          >
            Architecture
          </a>
          <a
            href="https://github.com/SriramWorkSpace/MedSpace-Healthcare/blob/main/docs/decisions.md"
            className="text-ink-2 hover:text-ink"
            target="_blank"
            rel="noreferrer"
          >
            Design decisions
          </a>
        </nav>
      </div>
      <div className="border-t border-line">
        <p className="mx-auto max-w-[1280px] px-4 py-5 text-xs text-ink-3 sm:px-6">
          © {new Date().getFullYear()} Sriram Madala · MIT License
        </p>
      </div>
    </footer>
  );
}
