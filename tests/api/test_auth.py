import sys
import pytest
from unittest import mock
from fastapi import HTTPException, status
from jose.exceptions import JWTError


mock_settings = mock.MagicMock()
mock_settings.SECRET_KEY = "testsecret"
mock_settings.ALGORITHM = "HS256"
mock_settings.DATABASE_URL = "postgresql://fake"

sys.modules["app.settings"] = mock.MagicMock(settings=mock_settings)

from app.api.auth import get_current_user


@pytest.mark.describe("Testes para get_current_user")
class TestGetCurrentUser:

    @pytest.mark.it("Deve retornar o usuário autenticado com token válido")
    @mock.patch("app.api.auth.get_user_by_email")
    @mock.patch("app.api.auth.decode_token")
    def test_get_current_user_success(self, mock_decode_token, mock_get_user_by_email):
        mock_token = "valid.token.here"
        mock_email = "test@example.com"
        mock_user = mock.MagicMock()
        mock_decode_token.return_value = {"sub": mock_email}
        mock_get_user_by_email.return_value = mock_user

        mock_db = mock.MagicMock()
        result = get_current_user(token=mock_token, db=mock_db)

        mock_decode_token.assert_called_once_with(mock_token)
        mock_get_user_by_email.assert_called_once_with(mock_db, mock_email)
        assert result == mock_user

    @pytest.mark.it("Deve lançar HTTP 401 se o campo 'sub' estiver ausente no token")
    @mock.patch("app.api.auth.decode_token")
    def test_get_current_user_missing_sub(self, mock_decode_token):
        mock_decode_token.return_value = {}
        mock_token = "invalid.token"

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=mock_token, db=mock.MagicMock())

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token inválido ou expirado" in exc_info.value.detail

    @pytest.mark.it("Deve lançar HTTP 401 se o token for inválido")
    @mock.patch("app.api.auth.decode_token", side_effect=JWTError("Token inválido"))
    def test_get_current_user_invalid_token(self, _):
        mock_token = "broken.token"

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=mock_token, db=mock.MagicMock())

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.it("Deve lançar HTTP 401 se o usuário não for encontrado")
    @mock.patch("app.api.auth.get_user_by_email", return_value=None)
    @mock.patch("app.api.auth.decode_token")
    def test_get_current_user_user_not_found(self, mock_decode_token, mock_get_user_by_email):
        mock_decode_token.return_value = {"sub": "user@example.com"}

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="token", db=mock.MagicMock())

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
