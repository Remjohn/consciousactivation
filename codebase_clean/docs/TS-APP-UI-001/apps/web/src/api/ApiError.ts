export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number | null,
    readonly errorCode: string | null,
    readonly service: string | null = null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
