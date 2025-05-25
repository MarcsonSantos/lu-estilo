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
from app.api.orders import create, list_all, get, update, delete


@pytest.mark.describe("Testes para rotas de pedidos")
class TestOrderRoutes:

    @pytest.mark.it("Deve criar pedido se for cliente autenticado")
    @mock.patch("app.api.orders.create_order", return_value="pedido_criado")
    def test_create_order_success(self, mock_create_order):
        mock_db = mock.MagicMock()
        mock_user = mock.MagicMock()
        mock_user.client.id = 1
        mock_client_order = mock.MagicMock()

        result = create(client_order=mock_client_order, db=mock_db, current_user=mock_user)

        mock_create_order.assert_called_once_with(mock_db, 1, mock_client_order)
        assert result == "pedido_criado"

    @pytest.mark.it("Deve negar criação se usuário não for cliente")
    def test_create_order_forbidden(self):
        mock_user = mock.MagicMock(client=None)

        with pytest.raises(HTTPException) as exc:
            create(client_order=mock.MagicMock(), db=mock.MagicMock(), current_user=mock_user)

        assert exc.value.status_code == 403

    @pytest.mark.it("Admin deve listar todos os pedidos")
    @mock.patch("app.api.orders.list_orders", return_value=["pedido1", "pedido2"])
    def test_list_all_admin(self, mock_list_orders):
        mock_user = mock.MagicMock(is_admin=True)
        mock_db = mock.MagicMock()

        result = list_all(skip=0, limit=10, db=mock_db, current_user=mock_user)

        mock_list_orders.assert_called_once_with(mock_db, 0, 10)
        assert result == ["pedido1", "pedido2"]

    @pytest.mark.it("Cliente deve listar apenas seus próprios pedidos")
    def test_list_all_cliente(self):
        mock_user = mock.MagicMock(is_admin=False)
        mock_user.client.id = 7
        mock_db = mock.MagicMock()

        mock_query = mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.offset.return_value.limit.return_value.all.return_value = ["pedido_cliente"]

        result = list_all(skip=0, limit=10, db=mock_db, current_user=mock_user)

        assert result == ["pedido_cliente"]

    @pytest.mark.it("Deve negar listagem se cliente não associado")
    def test_list_all_forbidden(self):
        mock_user = mock.MagicMock(is_admin=False, client=None)

        with pytest.raises(HTTPException) as exc:
            list_all(skip=0, limit=10, db=mock.MagicMock(), current_user=mock_user)

        assert exc.value.status_code == 403

    @pytest.mark.it("Admin pode acessar qualquer pedido")
    @mock.patch("app.api.orders.get_order_by_id", return_value="pedido_admin")
    def test_get_order_admin(self, mock_get_order):
        mock_user = mock.MagicMock(is_admin=True)
        result = get(id=1, db=mock.MagicMock(), current_user=mock_user)
        assert result == "pedido_admin"

    @pytest.mark.it("Cliente pode acessar seu próprio pedido")
    @mock.patch("app.api.orders.get_order_by_id")
    def test_get_order_client(self, mock_get_order):
        mock_order = mock.MagicMock(client_id=7)
        mock_get_order.return_value = mock_order
        mock_user = mock.MagicMock(is_admin=False)
        mock_user.client.id = 7

        result = get(id=5, db=mock.MagicMock(), current_user=mock_user)
        assert result == mock_order

    @pytest.mark.it("Deve negar acesso ao pedido de outro cliente")
    @mock.patch("app.api.orders.get_order_by_id")
    def test_get_order_access_denied(self, mock_get_order):
        mock_get_order.return_value = mock.MagicMock(client_id=9)
        mock_user = mock.MagicMock(is_admin=False)
        mock_user.client.id = 99

        with pytest.raises(HTTPException) as exc:
            get(id=2, db=mock.MagicMock(), current_user=mock_user)

        assert exc.value.status_code == 403

    @pytest.mark.it("Deve atualizar pedido se for admin")
    @mock.patch("app.api.orders.update_order", return_value="pedido_atualizado")
    @mock.patch("app.api.orders.get_order_by_id")
    def test_update_order_admin(self, mock_get_order, mock_update_order):
        mock_get_order.return_value = mock.MagicMock(client_id=1)
        mock_user = mock.MagicMock(is_admin=True)
        mock_order_in = mock.MagicMock()

        result = update(id=1, order_in=mock_order_in, db=mock.MagicMock(), current_user=mock_user)
        assert result == "pedido_atualizado"

    @pytest.mark.it("Deve excluir pedido se for admin")
    @mock.patch("app.api.orders.delete_order")
    @mock.patch("app.api.orders.get_order_by_id")
    def test_delete_order_admin(self, mock_get_order, mock_delete_order):
        mock_get_order.return_value = mock.MagicMock(client_id=1)
        mock_user = mock.MagicMock(is_admin=True)

        result = delete(id=1, db=mock.MagicMock(), current_user=mock_user)

        mock_delete_order.assert_called_once()
        assert result == {"message": "Pedido excluído com sucesso"}
