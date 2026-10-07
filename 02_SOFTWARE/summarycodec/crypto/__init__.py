"""Cryptographic integrity: SHA-256 hash chain + Ed25519 signatures.

Uses the `cryptography` library only; no invented algorithms.
"""

from __future__ import annotations

import base64
import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    priv = Ed25519PrivateKey.generate()
    return priv, priv.public_key()


def public_key_pem(pub: Ed25519PublicKey) -> str:
    return pub.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def load_public_key(pem: str) -> Ed25519PublicKey:
    return serialization.load_pem_public_key(pem.encode("ascii"))


def signed_digest(manifest_hash: str, payload_hash: str) -> bytes:
    """The bytes actually signed: SHA256(manifest_hash || payload_hash)."""
    raw = (manifest_hash + payload_hash).encode("ascii")
    return hashlib.sha256(raw).digest()


def sign(priv: Ed25519PrivateKey, manifest_hash: str, payload_hash: str) -> str:
    sig = priv.sign(signed_digest(manifest_hash, payload_hash))
    return base64.b64encode(sig).decode("ascii")


def verify(pub: Ed25519PublicKey, manifest_hash: str, payload_hash: str,
           sig_b64: str) -> bool:
    try:
        pub.verify(base64.b64decode(sig_b64),
                   signed_digest(manifest_hash, payload_hash))
        return True
    except Exception:
        return False
