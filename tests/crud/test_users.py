import sys
import pytest
from unittest import mock

mock_settings = mock.MagicMock()
mock_settings.SECRET_KEY = "testsecret"
mock_settings.ALGORITHM = "HS256"
mock_settings.DATABASE_URL = "postgresql://fake"

sys.modules["app.settings"] = mock.MagicMock(settings=mock_settings)

from app.crud.users import User, get_user_by_id, get_user_by_email, get_user_by_cpf, create_user


@pytest.mark.describe("get_user_by_id")
class TestGetUserById:
    @pytest.mark.it("Deve retornar o usuário pelo ID")
    def test_get_user_by_id(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_user = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_user

        result = get_user_by_id(mock_db, 1)

        mock_db.query.assert_called_once_with(User)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_user


@pytest.mark.describe("get_user_by_email")
class TestGetUserByEmail:
    @pytest.mark.it("Deve retornar o usuário pelo email")
    def test_get_user_by_email(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_user = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_user

        result = get_user_by_email(mock_db, "exemplo@email.com")

        mock_db.query.assert_called_once_with(User)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_user


@pytest.mark.describe("get_user_by_cpf")
class TestGetUserByCpf:
    @pytest.mark.it("Deve retornar o usuário pelo CPF")
    def test_get_user_by_cpf(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_user = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_user

        result = get_user_by_cpf(mock_db, "12345678900")

        mock_db.query.assert_called_once_with(User)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_user


@pytest.mark.describe("create_user")
class TestCreateUser:
    @pytest.mark.it("Deve criar um novo usuário com senha criptografada")
    def test_create_user(self):
        mock_db = mock.MagicMock()
        mock_user_data = mock.MagicMock(email="exemplo@email.com", cpf="12345678900", password="senha123")
        mock_user = mock.MagicMock()

        with mock.patch("app.crud.users.get_password_hash", return_value="hashed123") as mock_hash:
            with mock.patch("app.crud.users.User", return_value=mock_user):
                result = create_user(mock_db, mock_user_data)

        mock_hash.assert_called_once_with("senha123")
        mock_db.add.assert_called_once_with(mock_user)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_user)
        assert result == mock_user