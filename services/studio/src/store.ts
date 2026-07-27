import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname } from "node:path";
import { canonicalJson, canonicalSha256, sha256Hex } from "./canonical.js";

export interface LedgerEntry<T> {
  readonly sequence: number;
  readonly previous_entry_sha256: string | null;
  readonly record_sha256: string;
  readonly entry_sha256: string;
  readonly record: T;
}

export class AppendOnlyJsonLedger<T> {
  readonly filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  readAll(): ReadonlyArray<LedgerEntry<T>> {
    if (!existsSync(this.filePath)) return [];
    const content = readFileSync(this.filePath, "utf8");
    if (!content.trim()) return [];
    const entries = content
      .split(/\r?\n/)
      .filter((line) => line.trim())
      .map((line) => JSON.parse(line) as LedgerEntry<T>);
    let previous: string | null = null;
    for (let index = 0; index < entries.length; index += 1) {
      const entry = entries[index]!;
      if (entry.sequence !== index + 1) throw new Error(`ledger sequence mismatch at ${index + 1}`);
      if (entry.previous_entry_sha256 !== previous) throw new Error(`ledger chain mismatch at ${entry.sequence}`);
      if (canonicalSha256(entry.record) !== entry.record_sha256) throw new Error(`ledger record hash mismatch at ${entry.sequence}`);
      const computed = canonicalSha256({ sequence: entry.sequence, previous_entry_sha256: entry.previous_entry_sha256, record_sha256: entry.record_sha256, record: entry.record });
      if (computed !== entry.entry_sha256) throw new Error(`ledger entry hash mismatch at ${entry.sequence}`);
      previous = entry.entry_sha256;
    }
    return entries;
  }

  append(record: T): LedgerEntry<T> {
    const entries = this.readAll();
    const sequence = entries.length + 1;
    const previous = entries.length ? entries[entries.length - 1]!.entry_sha256 : null;
    const recordSha = canonicalSha256(record);
    const body = { sequence, previous_entry_sha256: previous, record_sha256: recordSha, record };
    const entry: LedgerEntry<T> = { ...body, entry_sha256: canonicalSha256(body) };
    mkdirSync(dirname(this.filePath), { recursive: true });
    appendFileSync(this.filePath, `${canonicalJson(entry)}\n`, { encoding: "utf8", flag: "a" });
    return entry;
  }

  fileSha256(): string | null {
    if (!existsSync(this.filePath)) return null;
    return sha256Hex(readFileSync(this.filePath, "utf8"));
  }
}
