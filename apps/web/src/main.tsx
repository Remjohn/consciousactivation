import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { QueryClientProvider } from "@tanstack/react-query";
import { routeTree } from "./routeTree.gen";
import { queryClient } from "./api/queryClient";
import { DevOperatorProvider } from "./auth/DevOperatorContext";
import "./styles/index.css";

const router = createRouter({ routeTree, defaultPreload: "intent" });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const rootElement = document.getElementById("root")!;
createRoot(rootElement).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <DevOperatorProvider>
        <RouterProvider router={router} />
      </DevOperatorProvider>
    </QueryClientProvider>
  </StrictMode>,
);
