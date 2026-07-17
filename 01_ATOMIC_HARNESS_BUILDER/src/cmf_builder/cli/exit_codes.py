from __future__ import annotations

from enum import IntEnum

from cmf_builder.application.productization_contracts import ProductizationErrorCode


class CLIExitCode(IntEnum):
    SUCCESS = 0
    USAGE = 2
    AUTHORITY_REJECTED = 3
    NOT_FOUND = 4
    CONFLICT = 5
    INTEGRITY_ERROR = 6
    EXPORT_REJECTED = 7
    INTERNAL_ERROR = 70


_ERROR_EXIT_CODES = {
    ProductizationErrorCode.INVALID_MANIFEST: CLIExitCode.USAGE,
    ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT: CLIExitCode.USAGE,
    ProductizationErrorCode.AUTHORITY_REJECTED: CLIExitCode.AUTHORITY_REJECTED,
    ProductizationErrorCode.HASH_MISMATCH: CLIExitCode.INTEGRITY_ERROR,
    ProductizationErrorCode.NOT_FOUND: CLIExitCode.NOT_FOUND,
    ProductizationErrorCode.CONFLICT: CLIExitCode.CONFLICT,
    ProductizationErrorCode.STORAGE_INTEGRITY: CLIExitCode.INTEGRITY_ERROR,
    ProductizationErrorCode.EXPORT_REJECTED: CLIExitCode.EXPORT_REJECTED,
    ProductizationErrorCode.INTERNAL_ERROR: CLIExitCode.INTERNAL_ERROR,
}


def exit_code_for_error(code: ProductizationErrorCode) -> CLIExitCode:
    return _ERROR_EXIT_CODES.get(code, CLIExitCode.INTERNAL_ERROR)
