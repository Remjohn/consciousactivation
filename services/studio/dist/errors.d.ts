export declare class StudioValidationError extends Error {
    readonly code: string;
    readonly context: Record<string, unknown>;
    constructor(code: string, message: string, context?: Record<string, unknown>);
}
