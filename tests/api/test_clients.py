import sys
from unittest import mock

# Mock do settings
mock_settings = mock.MagicMock()
mock_settings.SECRET_KEY = "fake"
mock_settings.ALGORITHM = "HS256"
mock_settings.DATABASE_URL = "postgresql://fake"
sys.modules["app.settings"] = mock.MagicMock(settings=mock_settings)

import pytest
from fastapi import HTTPException
from unittest import mock
from app.api.clients import list_clients, create_new_client, get_client, update_client, delete_client
from app.schemas.clients import ClientUpdate


@pytest.mark.describe("Testes para rotas de clientes")
class TestClient:

    @pytest.mark.it("Deve listar clientes quando o usuário for admin")
    def test_list_clients_admin(self):
        mock_db = mock.MagicMock()
        mock_user = mock.MagicMock(is_admin=True)
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.offset.return_value.limit.return_value.all.return_value = ["cliente1", "cliente2"]

        result = list_clients(name="cli", skip=0, limit=10, db=mock_db, current_user=mock_user)
        assert result == ["cliente1", "cliente2"]

    @pytest.mark.it("Deve negar acesso à listagem de clientes para não admin")
    def test_list_clients_non_admin(self):
        with pytest.raises(HTTPException) as exc:
            list_clients(name=None, skip=0, limit=10, db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=False))
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve criar novo cliente com dados válidos")
    @mock.patch("app.crud.users.create_user")
    @mock.patch("app.api.clients.create_client")
    @mock.patch("app.api.clients.get_user_by_cpf")
    @mock.patch("app.api.clients.get_user_by_email")
    def test_create_new_client_success(self, mock_get_email, mock_get_cpf, mock_create_client, mock_create_user):
        mock_db = mock.MagicMock()

        mock_get_email.return_value = None
        mock_get_cpf.return_value = None

        mock_user = mock.MagicMock()
        mock_user.id = 123
        mock_create_user.return_value = mock_user

        mock_create_client.return_value = "novo_cliente"

        mock_client_in = mock.MagicMock()
        mock_client_in.email = "test@test.com"
        mock_client_in.cpf = "12345678900"

        result = create_new_client(mock_client_in, db=mock_db)

        mock_get_email.assert_called_once_with(mock_db, "test@test.com")
        mock_get_cpf.assert_called_once_with(mock_db, "12345678900")
        mock_create_user.assert_called_once_with(mock_db, mock_client_in)
        mock_create_client.assert_called_once_with(mock_db, mock_client_in, user_id=123)
        assert result == "novo_cliente"

    @pytest.mark.it("Deve lançar erro se email já estiver cadastrado")
    @mock.patch("app.api.clients.get_user_by_email", return_value=True)
    @mock.patch("app.api.clients.get_user_by_cpf")
    @mock.patch("app.crud.users.create_user")
    @mock.patch("app.crud.clients.create_client")
    def test_create_client_email_in_use(self, mock_create_client, mock_create_user, mock_get_cpf, mock_get_email):
        mock_db = mock.MagicMock()

        mock_get_email.return_value = True

        mock_client_in = mock.MagicMock()
        mock_client_in.email = "a@a.com"
        mock_client_in.cpf = "1"

        with pytest.raises(HTTPException) as exc:
            create_new_client(mock_client_in, db=mock_db)

        assert exc.value.status_code == 400
        assert exc.value.detail == "Email já está em uso."

        mock_get_cpf.assert_not_called()
        mock_create_user.assert_not_called()
        mock_create_client.assert_not_called()

    @pytest.mark.it("Deve lançar erro se CPF já estiver cadastrado")
    @mock.patch("app.crud.users.create_user")
    @mock.patch("app.crud.clients.create_client")
    @mock.patch("app.api.clients.get_user_by_cpf", return_value=True)
    @mock.patch("app.api.clients.get_user_by_email", return_value=None)
    def test_create_client_cpf_in_use(self, mock_get_email, mock_get_cpf, mock_create_client, mock_create_user):
        mock_db = mock.MagicMock()

        mock_client_in = mock.MagicMock()
        mock_client_in.email = "a@a.com"
        mock_client_in.cpf = "1"

        with pytest.raises(HTTPException) as exc:
            create_new_client(mock_client_in, db=mock_db)

        assert exc.value.status_code == 400
        assert exc.value.detail == "CPF já está em uso."

        mock_create_user.assert_not_called()
        mock_create_client.assert_not_called()

    @pytest.mark.it("Deve retornar cliente se usuário for admin")
    @mock.patch("app.api.clients.get_client_by_id")
    def test_get_client_admin(self, mock_get_client):
        mock_db = mock.MagicMock()
        mock_client = mock.MagicMock(user_id=2)
        mock_user = mock.MagicMock(id=1, is_admin=True)
        mock_get_client.return_value = mock_client

        result = get_client(id=2, db=mock_db, current_user=mock_user)
        assert result == mock_client

    @pytest.mark.it("Deve lançar erro se cliente não for encontrado")
    @mock.patch("app.api.clients.get_client_by_id", return_value=None)
    def test_get_client_not_found(self, _):
        with pytest.raises(HTTPException) as exc:
            get_client(id=99, db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=True))
        assert exc.value.status_code == 404

    @pytest.mark.it("Deve negar acesso ao cliente se não for admin nem o dono")
    @mock.patch("app.api.clients.get_client_by_id")
    def test_get_client_access_denied(self, mock_get_client):
        mock_get_client.return_value = mock.MagicMock(user_id=2)
        with pytest.raises(HTTPException) as exc:
            get_client(id=2, db=mock.MagicMock(), current_user=mock.MagicMock(id=3, is_admin=False))
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve atualizar cliente se usuário for admin")
    @mock.patch("app.api.clients.get_client_by_id")
    def test_update_client_admin(self, mock_get_client):
        mock_client = mock.MagicMock()
        mock_get_client.return_value = mock_client
        mock_db = mock.MagicMock()
        update_data = ClientUpdate(name="Novo Nome", phone_number="", address="")

        result = update_client(id=1, client_in=update_data, db=mock_db, current_user=mock.MagicMock(is_admin=True))
        assert result == mock_client

    @pytest.mark.it("Deve excluir cliente se for admin")
    @mock.patch("app.api.clients.get_client_by_id")
    def test_delete_client_admin(self, mock_get_client):
        mock_client = mock.MagicMock()
        mock_get_client.return_value = mock_client
        mock_db = mock.MagicMock()
        mock_user = mock.MagicMock(is_admin=True)

        delete_client(id=1, db=mock_db, current_user=mock_user)
        mock_db.delete.assert_called_once_with(mock_client)
        mock_db.commit.assert_called_once()

    @pytest.mark.it("Deve negar exclusão de cliente para não admin")
    def test_delete_client_not_admin(self):
        with pytest.raises(HTTPException) as exc:
            delete_client(id=1, db=mock.MagicMock(), current_user=mock.MagicMock(is_admin=False))
        assert exc.value.status_code == 403
