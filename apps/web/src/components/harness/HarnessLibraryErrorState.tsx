import type { ApiError } from "../../api/ApiError";

export function HarnessLibraryErrorState({ error }: { readonly error: ApiError }) {
  const isUnreachable = error.status === null;

  return (
    <div className="p-8" role="alert">
      <p className="text-lg font-semibold text-danger">
        {isUnreachable ? "Gateway unreachable" : "The harness library could not be read"}
      </p>
      <p className="mt-2 text-sm text-muted-foreground">
        {isUnreachable
          ? "The API gateway did not respond — is it running?"
          : error.message}
      </p>
    </div>
  );
}
