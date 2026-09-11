export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | ReadonlyArray<JsonValue> | {
    readonly [key: string]: JsonValue;
};
export declare function canonicalJson(value: unknown): string;
export declare function sha256Hex(value: string | Uint8Array): string;
export declare function canonicalSha256(value: unknown): string;
export declare function deterministicId(prefix: string, value: unknown): string;
export declare function assertPortableUri(uri: string): void;
export declare function assertSha256(value: string, label?: string): void;
export declare function uniqueSorted(values: ReadonlyArray<string>): ReadonlyArray<string>;
export declare function tokenize(value: string): ReadonlyArray<string>;
