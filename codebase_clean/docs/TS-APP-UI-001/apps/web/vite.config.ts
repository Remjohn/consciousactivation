import { defineConfig } from "vite";
import path from "node:path";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";

const repoRoot = path.resolve(__dirname, "../..");

export default defineConfig({
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
      routeFileIgnorePattern: "\\.test\\.tsx$",
    }),
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@ca/studio": path.resolve(repoRoot, "services/studio/src"),
    },
  },
  server: {
    port: 5173,
    fs: {
      // services/studio/src sits outside apps/web/ — Vite's dev server refuses to
      // serve files outside its root unless explicitly allowed. See Section 3.
      allow: [repoRoot],
    },
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
