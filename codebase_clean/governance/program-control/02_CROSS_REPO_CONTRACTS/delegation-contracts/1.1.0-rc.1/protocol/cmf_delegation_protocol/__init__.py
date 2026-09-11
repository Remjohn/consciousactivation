"""CMF delegation Stage 5 transport-neutral reference package."""

from .clock import FrozenClock, SystemClock
from .engine import ProtocolEngine
from .errors import PersistenceError, ProtocolRejection
from .signing import Ed25519KeyRegistry, sign_envelope
from .store import InMemoryProtocolStore

__all__ = [
    "Ed25519KeyRegistry",
    "FrozenClock",
    "InMemoryProtocolStore",
    "PersistenceError",
    "ProtocolEngine",
    "ProtocolRejection",
    "SystemClock",
    "sign_envelope",
]

