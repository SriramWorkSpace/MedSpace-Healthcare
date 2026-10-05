import { createBrowserRouter } from "react-router";
import MarketingLayout from "./layouts/MarketingLayout";
import RouteError from "./RouteError";
import Landing from "@/pages/marketing/Landing";

/** Route modules are code-split; each lazy() resolves to `{ Component }`. */
const page = (loader) => async () => ({ Component: (await loader()).default });
/** Layouts too, so the landing page doesn't download the app shell (search, nav, banners). */
const appLayout = page(() => import("./layouts/AppLayout"));
const authLayout = page(() => import("./layouts/AuthLayout"));
const openAuthLayout = async () => {
  const { default: AuthLayout } = await import("./layouts/AuthLayout");
  return { Component: () => <AuthLayout open /> };
};

export const router = createBrowserRouter([
  {
    errorElement: <RouteError />,
    children: [
      {
        element: <MarketingLayout />,
        children: [{ index: true, element: <Landing /> }],
      },
      {
        lazy: authLayout,
        children: [
          { path: "login", lazy: page(() => import("@/pages/auth/Login")) },
          { path: "signup", lazy: page(() => import("@/pages/auth/Signup")) },
          { path: "forgot-password", lazy: page(() => import("@/pages/auth/ForgotPassword")) },
        ],
      },
      {
        // Emailed links: they must work whether or not this browser is signed in.
        lazy: openAuthLayout,
        children: [
          { path: "reset-password", lazy: page(() => import("@/pages/auth/ResetPassword")) },
          { path: "verify-email", lazy: page(() => import("@/pages/auth/VerifyEmail")) },
          {
            path: "confirm-email-change",
            lazy: page(() => import("@/pages/auth/ConfirmEmailChange")),
          },
        ],
      },
      {
        path: "app",
        lazy: appLayout,
        children: [
          { index: true, lazy: page(() => import("@/pages/app/Dashboard")) },
          { path: "documents", lazy: page(() => import("@/pages/app/Documents")) },
          { path: "documents/:id", lazy: page(() => import("@/pages/app/DocumentReview")) },
          { path: "prescriptions/:id", lazy: page(() => import("@/pages/app/PrescriptionReport")) },
          { path: "medications", lazy: page(() => import("@/pages/app/Medications")) },
          {
            path: "medications/:id",
            lazy: page(() => import("@/pages/app/MedicationHistory")),
          },
          { path: "labs", lazy: page(() => import("@/pages/app/Labs")) },
          { path: "labs/:key", lazy: page(() => import("@/pages/app/LabDetail")) },
          { path: "diet", lazy: page(() => import("@/pages/app/Diet")) },
          { path: "timeline", lazy: page(() => import("@/pages/app/Timeline")) },
          { path: "visits", lazy: page(() => import("@/pages/app/Visits")) },
          { path: "visits/:id", lazy: page(() => import("@/pages/app/VisitPrep")) },
          { path: "ask", lazy: page(() => import("@/pages/app/Ask")) },
          { path: "sharing", lazy: page(() => import("@/pages/app/Sharing")) },
          { path: "settings", lazy: page(() => import("@/pages/app/Settings")) },
          {
            path: "circle/accept/:token",
            lazy: page(() => import("@/pages/app/CircleAccept")),
          },
        ],
      },
      { path: "s/:token", lazy: page(() => import("@/pages/share/SharedView")) },
      { path: "*", lazy: page(() => import("@/pages/NotFound")) },
    ],
  },
]);
