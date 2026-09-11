import { createHash } from "node:crypto";
function normalize(value, path = "$") {
    if (value === null || typeof value === "string" || typeof value === "boolean") {
        return value;
    }
    if (typeof value === "number") {
        if (!Number.isSafeInteger(value)) {
            throw new TypeError(`${path}: canonical numbers must be safe integers`);
        }
        return value;
    }
    if (Array.isArray(value)) {
        return value.map((item, index) => normalize(item, `${path}[${index}]`));
    }
    if (typeof value === "object") {
        const object = value;
        const result = {};
        for (const key of Object.keys(object).sort()) {
            const item = object[key];
            if (item === undefined) {
                throw new TypeError(`${path}.${key}: undefined is not canonical`);
            }
            result[key] = normalize(item, `${path}.${key}`);
        }
        return result;
    }
    throw new TypeError(`${path}: unsupported canonical value ${typeof value}`);
}
export function canonicalJson(value) {
    return JSON.stringify(normalize(value));
}
export function sha256Hex(value) {
    return createHash("sha256").update(value).digest("hex");
}
export function canonicalSha256(value) {
    return sha256Hex(canonicalJson(value));
}
export function deterministicId(prefix, value) {
    if (!/^[a-z0-9][a-z0-9._:-]*$/i.test(prefix)) {
        throw new TypeError(`invalid deterministic ID prefix: ${prefix}`);
    }
    return `${prefix}:${canonicalSha256(value).slice(0, 24)}`;
}
export function assertPortableUri(uri) {
    if (!uri || uri.startsWith("/") || uri.includes("\\") || /^[A-Za-z]:\//.test(uri) || uri.includes("..")) {
        throw new TypeError(`non-portable URI: ${uri}`);
    }
}
export function assertSha256(value, label = "sha256") {
    if (!/^[0-9a-f]{64}$/.test(value)) {
        throw new TypeError(`${label} must be lowercase SHA-256`);
    }
}
export function uniqueSorted(values) {
    return [...new Set(values)].sort();
}
export function tokenize(value) {
    return uniqueSorted(value
        .toLocaleLowerCase("en-US")
        .normalize("NFKD")
        .replace(/[^a-z0-9:_-]+/g, " ")
        .trim()
        .split(/\s+/)
        .filter((token) => token.length >= 2));
}
