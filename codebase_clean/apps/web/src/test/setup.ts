import "@testing-library/jest-dom/vitest";

// TanStack Router runs scroll-restoration on navigation, which calls window.scrollTo.
// jsdom does not implement window.scrollTo and logs a noisy "Not implemented" warning
// per navigation. Stub it so route-level tests stay quiet and behaviour is preserved.
if (typeof window !== "undefined" && typeof window.scrollTo !== "function") {
  window.scrollTo = (() => {}) as typeof window.scrollTo;
}
