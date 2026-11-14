"""Pure-stdlib Ed25519 (RFC 8032) for the Receipts demo prototype only.

DEMO ONLY. This is a teaching/prototype implementation, not a
production-grade cryptographic library. It is used here so the
prototype runs on Python's standard library alone, with no installs,
no network calls, and no Meta API calls.

The implementation is checked against the RFC 8032 test vector in
test_receipts.py. Do not reuse these demo keys for anything real,
and never use a production or verify-atom key here.
"""

import hashlib
import os

B = 256
Q = 2 ** 255 - 19
L = 2 ** 252 + 27742317777372353535851937790883648493
D = (-121665 * pow(121666, Q - 2, Q)) % Q
I = pow(2, (Q - 1) // 4, Q)


def _sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def _expmod(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)


def _inv(x: int) -> int:
    return pow(x, Q - 2, Q)


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * _inv(D * y * y + 1) % Q
    x = pow(xx, (Q + 3) // 8, Q)
    if (x * x - xx) % Q != 0:
        x = (x * I) % Q
    if x % 2 != 0:
        x = Q - x
    return x


# Base point, in extended coordinates (x, y, z, t) with x=X/Z etc.
_BY = (4 * _inv(5)) % Q
_BX = _xrecover(_BY)
_BASE = (_BX % Q, _BY % Q, 1, (_BX * _BY) % Q)


def _edwards(p, q):
    x1, y1, z1, t1 = p
    x2, y2, z2, t2 = q
    # Standard extended-coordinate addition (Hisil et al.).
    a = (x1 * x2) % Q
    b = (y1 * y2) % Q
    c = (t1 * D * t2) % Q
    d = (z1 * z2) % Q
    e = ((x1 + y1) * (x2 + y2) - a - b) % Q
    f = (d - c) % Q
    g = (d + c) % Q
    # Curve parameter a = -1, so the Hisil formula's "b - a_curve*a"
    # is b + a here. Using b - a gives points off the curve.
    h = (b + a) % Q
    return ((e * f) % Q, (g * h) % Q, (f * g) % Q, (e * h) % Q)


def _scalarmult(p, e: int):
    if e == 0:
        return (0, 1, 1, 0)
    q = _scalarmult(p, e // 2)
    q = _edwards(q, q)
    if e & 1:
        q = _edwards(q, p)
    return q


def _encodeint(y: int) -> bytes:
    return y.to_bytes(32, "little")


def _encodepoint(p) -> bytes:
    x, y, z, _t = p
    inv_z = _inv(z)
    ax = (x * inv_z) % Q
    ay = (y * inv_z) % Q
    bits = ay | ((ax & 1) << 255)
    return bits.to_bytes(32, "little")


def _decodeint(data: bytes) -> int:
    return int.from_bytes(data, "little")


def _decodepoint(data: bytes):
    y = _decodeint(data) & ((1 << 255) - 1)
    x = _xrecover(y)
    if x & 1 != (data[31] >> 7):
        x = Q - x
    return (x, y, 1, (x * y) % Q)


def _hint(data: bytes) -> int:
    h = _sha512(data)
    return int.from_bytes(h, "little")


def publickey_from_seed(seed: bytes) -> bytes:
    """Return the 32-byte public key for a 32-byte seed."""
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes")
    h = _sha512(seed)
    a = _decodeint(h[:32])
    a &= (1 << 254) - 8
    a |= 1 << 254
    return _encodepoint(_scalarmult(_BASE, a))


def sign(message: bytes, seed: bytes, public_key: bytes) -> bytes:
    """Return a 64-byte Ed25519 signature for message."""
    if len(seed) != 32:
        raise ValueError("seed must be 32 bytes")
    h = _sha512(seed)
    a = _decodeint(h[:32])
    a &= (1 << 254) - 8
    a |= 1 << 254
    r = _hint(h[32:] + message) % L
    r_point = _encodepoint(_scalarmult(_BASE, r))
    s = (_hint(r_point + public_key + message) * a + r) % L
    return r_point + _encodeint(s)


def verify(signature: bytes, message: bytes, public_key: bytes) -> bool:
    """Return True only if signature is valid for message under public_key."""
    if len(signature) != 64 or len(public_key) != 32:
        return False
    try:
        r_point = _decodepoint(signature[:32])
        a_point = _decodepoint(public_key)
        s = _decodeint(signature[32:])
    except Exception:
        return False
    if s >= L:
        return False
    h = _hint(signature[:32] + public_key + message) % L
    # Check: s*B == R + h*A
    left = _scalarmult(_BASE, s)
    right = _edwards(r_point, _scalarmult(a_point, h))
    # Compare in affine form.
    def affine(p):
        inv_z = _inv(p[2])
        return ((p[0] * inv_z) % Q, (p[1] * inv_z) % Q)

    return affine(left) == affine(right)


def generate_seed() -> bytes:
    return os.urandom(32)
