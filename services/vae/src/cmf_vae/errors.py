class VAEError(RuntimeError):
    pass


class VAEValidationError(VAEError, ValueError):
    pass


class QueueConflict(VAEError):
    pass


class LeaseConflict(VAEError):
    pass


class CapabilityGap(VAEError):
    pass
