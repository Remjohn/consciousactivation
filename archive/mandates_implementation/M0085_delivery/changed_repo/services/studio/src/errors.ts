export class StudioValidationError extends Error {
  readonly code: string;
  readonly context: Record<string, unknown>;
  constructor(code: string, message: string, context: Record<string, unknown> = {}) {
    super(message);
    this.name = "StudioValidationError";
    this.code = code;
    this.context = context;
  }
}
