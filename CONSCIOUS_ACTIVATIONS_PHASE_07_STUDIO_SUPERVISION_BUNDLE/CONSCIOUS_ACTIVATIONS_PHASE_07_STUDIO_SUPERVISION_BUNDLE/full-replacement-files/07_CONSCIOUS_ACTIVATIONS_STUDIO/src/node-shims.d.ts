declare module "node:crypto" {
  export function createHash(algorithm: string): {
    update(data: string | Uint8Array): ReturnType<typeof createHash>;
    digest(encoding: "hex"): string;
  };
}

declare module "node:fs" {
  export function appendFileSync(path: string, data: string, options?: { encoding?: string; flag?: string }): void;
  export function existsSync(path: string): boolean;
  export function mkdirSync(path: string, options?: { recursive?: boolean }): string | undefined;
  export function readFileSync(path: string, encoding: "utf8"): string;
  export function writeFileSync(path: string, data: string, encoding: "utf8"): void;
}

declare module "node:path" {
  export function dirname(path: string): string;
  export function join(...parts: string[]): string;
  export function resolve(...parts: string[]): string;
}

declare const process: {
  argv: string[];
  exitCode?: number;
  cwd(): string;
};
