import sys
import pytest
from unittest import mock

mock_settings = mock.MagicMock()
mock_settings.SECRET_KEY = "testsecret"
mock_settings.ALGORITHM = "HS256"
mock_settings.DATABASE_URL = "postgresql://fake"

sys.modules["app.settings"] = mock.MagicMock(settings=mock_settings)

from app.core.security import get_password_hash, verify_password


@pytest.mark.describe("get_password_hash")
class TestGetPasswordHash:
    @pytest.mark.it("Deve retornar um hash para a senha")
    def test_get_password_hash(self):
        with mock.patch("app.core.security.pwd_context.hash", return_value="hashed_password") as mock_hash:
            result = get_password_hash("senha123")
            mock_hash.assert_called_once_with("senha123")
            assert result == "hashed_password"


@pytest.mark.describe("verify_password")
class TestVerifyPassword:
    @pytest.mark.it("Deve retornar True se a senha for válida")
    def test_verify_password_true(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=True) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is True

    @pytest.mark.it("Deve retornar False se a senha for inválida")
    def test_verify_password_false(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=False) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is False


@pytest.mark.describe("verify_password")
class TestVerifyPassword:
    @pytest.mark.it("Deve retornar True se a senha for válida")
    def test_verify_password_true(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=True) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is True

    @pytest.mark.it("Deve retornar False se a senha for inválida")
    def test_verify_password_false(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=False) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is False


@pytest.mark.describe("verify_password")
class TestVerifyPassword:
    @pytest.mark.it("Deve retornar True se a senha for válida")
    def test_verify_password_true(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=True) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is True

    @pytest.mark.it("Deve retornar False se a senha for inválida")
    def test_verify_password_false(self):
        with mock.patch("app.core.security.pwd_context.verify", return_value=False) as mock_verify:
            result = verify_password("senha123", "hashed")
            mock_verify.assert_called_once_with("senha123", "hashed")
            assert result is False