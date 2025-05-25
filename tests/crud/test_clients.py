import pytest
from unittest import mock
from app.db.models.clients import Client
from app.schemas.clients import ClientCreate
from app.crud.clients import (
    get_client_by_id,
    get_client_by_name,
    get_client_by_address,
    get_client_by_phone_number,
    get_client_by_user_id,
    create_client,
)


@pytest.mark.describe("get_client_by_id")
class TestGetClientById:
    @pytest.mark.it("Deve retornar o cliente pelo ID")
    def test_get_client_by_id(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_client = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_client

        result = get_client_by_id(mock_db, 1)

        mock_db.query.assert_called_once_with(Client)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_client


@pytest.mark.describe("get_client_by_name")
class TestGetClientByName:
    @pytest.mark.it("Deve retornar lista de clientes por nome")
    def test_get_client_by_name(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_clients = [mock.MagicMock()]

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.all.return_value = expected_clients

        result = get_client_by_name(mock_db, "João")

        mock_db.query.assert_called_once_with(Client)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
        assert result == expected_clients



@pytest.mark.describe("get_client_by_address")
class TestGetClientByAddress:
    @pytest.mark.it("Deve retornar lista de clientes por endereço")
    def test_get_client_by_address(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_clients = [mock.MagicMock()]

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.all.return_value = expected_clients

        result = get_client_by_address(mock_db, "Rua das Ninfas")

        mock_db.query.assert_called_once_with(Client)
        mock_query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
        assert result == expected_clients



@pytest.mark.describe("get_client_by_phone_number")
class TestGetClientByPhoneNumber:
    @pytest.mark.it("Deve retornar cliente pelo telefone")
    def test_get_client_by_phone_number(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_client = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_client

        result = get_client_by_phone_number(mock_db, "123456789")

        mock_db.query.assert_called_once_with(Client)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_client



@pytest.mark.describe("get_client_by_user_id")
class TestGetClientByUserId:
    @pytest.mark.it("Deve retornar cliente pelo ID do usuário")
    def test_get_client_by_user_id(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_client = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_client

        result = get_client_by_user_id(mock_db, 10)

        mock_db.query.assert_called_once_with(Client)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_client



@pytest.mark.describe("create_client")
class TestCreateClient:
    @pytest.mark.it("Deve criar e retornar um novo cliente")
    def test_create_client(self):
        mock_db = mock.MagicMock()
        client_data = ClientCreate(name="Maria", email="Maria@email.com", password="123456", cpf="423525234234", address="Rua A", phone_number="999999")
        mock_client = mock.MagicMock()

        # Mocka o construtor da classe Client para retornar o mock_client
        with mock.patch("app.crud.clients.Client", return_value=mock_client):
            result = create_client(mock_db, client_data, user_id=42)

        mock_db.add.assert_called_once_with(mock_client)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_client)
        assert result == mock_client

