import sys
import pytest
from unittest import mock

# Mock do settings
mock_settings = mock.MagicMock()
mock_settings.SECRET_KEY = "fake"
mock_settings.ALGORITHM = "HS256"
mock_settings.DATABASE_URL = "postgresql://fake"
sys.modules["app.settings"] = mock.MagicMock(settings=mock_settings)

from fastapi import HTTPException
from app.api.users import list_users, get_user, register, login, refresh_token


@pytest.mark.describe("Testes para rotas de autenticação")
class TestAuthUsersRoutes:

    @pytest.mark.it("Deve listar usuários se for admin")
    def test_list_users_admin(self):
        mock_user = mock.MagicMock(is_admin=True)
        mock_db = mock.MagicMock()
        mock_db.query.return_value.all.return_value = ["user1", "user2"]

        result = list_users(current_user=mock_user, db=mock_db)
        assert result == ["user1", "user2"]

    @pytest.mark.it("Deve negar listagem se não for admin")
    def test_list_users_forbidden(self):
        with pytest.raises(HTTPException) as exc:
            list_users(current_user=mock.MagicMock(is_admin=False), db=mock.MagicMock())
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve buscar usuário por ID")
    @mock.patch("app.api.users.get_user_by_id", return_value="user")
    def test_get_user_by_id(self, mock_get_id):
        result = get_user(id=1, db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=True))
        mock_get_id.assert_called_once()
        assert result == "user"

    @mock.patch("app.api.users.get_user_by_email", return_value="user")
    def test_get_user_by_email(self, mock_get_email):
        mock_db = mock.MagicMock()
        mock_admin = mock.MagicMock(is_admin=True)

        result = get_user(id=None, email="x@x.com", cpf=None, db=mock_db, current_user=mock_admin)

        mock_get_email.assert_called_once_with(mock_db, "x@x.com")
        assert result == "user"

    @pytest.mark.it("Deve buscar usuário por cpf")
    @mock.patch("app.api.users.get_user_by_cpf", return_value="user")
    def test_get_user_by_cpf(self, mock_get_cpf):
        mock_db = mock.MagicMock()
        mock_admin = mock.MagicMock(is_admin=True)

        result = get_user(id=None, email=None, cpf="12345678909", db=mock_db, current_user=mock_admin)

        mock_get_cpf.assert_called_once_with(mock_db, "12345678909")
        assert result == "user"

    @pytest.mark.it("Deve retornar erro se não passar id, email ou cpf")
    def test_get_user_missing_params(self):
        with pytest.raises(HTTPException) as exc:
            get_user(id=None, email=None, cpf=None, db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=True))
        assert exc.value.status_code == 400

    @pytest.mark.it("Deve negar busca se não for admin")
    def test_get_user_forbidden(self):
        with pytest.raises(HTTPException) as exc:
            get_user(email="x@x.com", db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=False))
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve registrar novo usuário se email não estiver em uso")
    @mock.patch("app.api.users.get_user_by_email", return_value=None)
    @mock.patch("app.api.users.create_user", return_value="novo_user")
    def test_register_success(self, mock_create_user, _):
        mock_db = mock.MagicMock()
        mock_user_in = mock.MagicMock(email="x@x.com")

        result = register(user_in=mock_user_in, db=mock_db)
        assert result == "novo_user"

    @pytest.mark.it("Deve retornar erro se email já estiver registrado")
    @mock.patch("app.api.auth.get_user_by_email", return_value="existe")
    def test_register_email_in_use(self, _):
        with pytest.raises(HTTPException) as exc:
            register(user_in=mock.MagicMock(email="x@x.com"), db=mock.MagicMock())
        assert exc.value.status_code == 400

    @pytest.mark.it("Deve fazer login com credenciais válidas")
    @mock.patch("app.api.users.create_access_token", return_value="token")
    @mock.patch("app.api.users.verify_password", return_value=True)
    @mock.patch("app.api.users.get_user_by_email")
    def test_login_success(self, mock_get_user, mock_verify, mock_create_token):
        mock_user = mock.MagicMock(email="x@x.com", hashed_password="hashed")
        mock_get_user.return_value = mock_user

        form = mock.MagicMock(username="x@x.com", password="123")
        result = login(form_data=form, db=mock.MagicMock())
        assert result == {"access_token": "token", "token_type": "bearer"}

    @pytest.mark.it("Deve retornar erro no login se credenciais inválidas")
    @mock.patch("app.api.users.verify_password", return_value=False)
    @mock.patch("app.api.auth.get_user_by_email")
    def test_login_invalid_credentials(self, mock_get_user, _):
        mock_get_user.return_value = mock.MagicMock()
        form = mock.MagicMock(username="x@x.com", password="errado")

        with pytest.raises(HTTPException) as exc:
            login(form_data=form, db=mock.MagicMock())
        assert exc.value.status_code == 401

    @pytest.mark.it("Deve gerar novo token se autenticado")
    @mock.patch("app.api.users.create_access_token", return_value="novo_token")
    def test_refresh_token(self, mock_create):
        user = mock.MagicMock(email="x@x.com")
        result = refresh_token(current_user=user)
        assert result == {"access_token": "novo_token", "token_type": "bearer"}
