"""Юніт-тести для core.security (хешування паролів і JWT)."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest

from core.config import settings
from core.security import create_access_token, get_password_hash, verify_password


def test_get_password_hash_returns_argon2_hash():
    hashed = get_password_hash("supersecret")

    assert hashed != "supersecret"
    assert hashed.startswith("$argon2")


def test_get_password_hash_is_salted():
    first = get_password_hash("same-password")
    second = get_password_hash("same-password")

    assert first != second


def test_verify_password_accepts_correct_password():
    hashed = get_password_hash("correct-horse")

    assert verify_password("correct-horse", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = get_password_hash("correct-horse")

    assert verify_password("wrong-horse", hashed) is False


def test_create_access_token_contains_subject_and_expiry():
    token = create_access_token(subject="user-123")

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload["sub"] == "user-123"
    assert "exp" in payload

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    assert abs((expires_at - expected).total_seconds()) < 60


def test_create_access_token_honours_custom_expiry():
    token = create_access_token(subject="user-123", expires_delta=timedelta(minutes=5))

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    assert expires_at - datetime.now(timezone.utc) < timedelta(minutes=6)


def test_expired_token_is_rejected():
    token = create_access_token(subject="user-123", expires_delta=timedelta(seconds=-1))

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def test_token_signed_with_other_key_is_rejected():
    token = create_access_token(subject="user-123")

    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "some-other-secret", algorithms=[settings.ALGORITHM])


def test_uuid_subject_is_converted_to_string():
    token = create_access_token(subject=42)

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload["sub"] == "42"
