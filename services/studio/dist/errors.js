export class StudioValidationError extends Error {
    code;
    context;
    constructor(code, message, context = {}) {
        super(message);
        this.name = "StudioValidationError";
        this.code = code;
        this.context = context;
    }
}
