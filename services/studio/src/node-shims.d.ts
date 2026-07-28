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
  // The return-type union is intentional: TS overloads readFileSync with both
  // an encoding-less form (returns Buffer) and an encoding form (returns
  // string).  Only the encoding form is used in this codebase; the Buffer
  // branch is declared as `unknown` so call sites that pass an encoding get
  // the string they expect without us lying about the no-encoding return.
  export function readFileSync(path: string): unknown;
  export function readFileSync(path: string, encoding: "utf8"): string;
  export function writeFileSync(path: string, data: string, encoding: "utf8"): void;
}

declare module "node:path" {
  export function dirname(path: string): string;
  export function join(...parts: string[]): string;
  export function resolve(...parts: string[]): string;
}

interface WritableStream {
  write(data: string): void;
}

interface ReadableStream {}

interface Process {
  argv: string[];
  exitCode?: number;
  cwd(): string;
  stdin: ReadableStream & { fd: number };
  stdout: WritableStream;
  stderr: WritableStream;
}

declare const process: Process;
