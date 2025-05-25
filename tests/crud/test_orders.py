import pytest
from unittest import mock
from fastapi import HTTPException
from app.crud.orders import Order, get_order_by_id, create_order, list_orders, update_order, delete_order


@pytest.mark.describe("create_order")
class TestCreateOrder:
    @pytest.mark.it("Deve criar pedido com item válido e estoque suficiente")
    def test_create_order_success(self):
        mock_db = mock.MagicMock()
        mock_product = mock.MagicMock(stock=10, description="Produto X", sale_price=50)
        mock_order = mock.MagicMock(id=123)

        mock_item = mock.MagicMock(product_id=1, quantity=2)
        mock_order_data = mock.MagicMock(items=[mock_item])

        mock_db.query.return_value.filter.return_value.first.return_value = mock_product

        with mock.patch("app.crud.orders.Order", return_value=mock_order), \
             mock.patch("app.crud.orders.OrderItem"):
            result = create_order(mock_db, client_id=1, order_data=mock_order_data)

        mock_db.add.assert_any_call(mock_order)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_order)
        assert result == mock_order

    @pytest.mark.it("Deve lançar 404 se produto não for encontrado")
    def test_create_order_product_not_found(self):
        mock_db = mock.MagicMock()

        mock_item = mock.MagicMock(product_id=1, quantity=2)
        mock_order_data = mock.MagicMock(items=[mock_item])

        mock_db.query.return_value.filter.return_value.first.return_value = None

        with mock.patch("app.crud.orders.Order"):
            with pytest.raises(HTTPException) as e:
                create_order(mock_db, 1, mock_order_data)

        assert e.value.status_code == 404
        assert "Produto ID" in e.value.detail

    @pytest.mark.it("Deve lançar 400 se estoque for zero")
    def test_create_order_stock_zero(self):
        mock_db = mock.MagicMock()

        mock_product = mock.MagicMock(stock=0, description="Produto Z")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product

        mock_item = mock.MagicMock(product_id=1, quantity=1)
        mock_order_data = mock.MagicMock(items=[mock_item])

        with mock.patch("app.crud.orders.Order"):
            with pytest.raises(HTTPException) as e:
                create_order(mock_db, 1, mock_order_data)

        assert e.value.status_code == 400
        assert "esgotado" in e.value.detail

    @pytest.mark.it("Deve lançar 400 se estoque for insuficiente")
    def test_create_order_insufficient_stock(self):
        mock_db = mock.MagicMock()

        mock_product = mock.MagicMock(stock=1, description="Produto Y")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product

        mock_item = mock.MagicMock(product_id=1, quantity=2)
        mock_order_data = mock.MagicMock(items=[mock_item])

        with mock.patch("app.crud.orders.Order"):
            with pytest.raises(HTTPException) as e:
                create_order(mock_db, 1, mock_order_data)

        assert e.value.status_code == 400
        assert "insuficiente" in e.value.detail

@pytest.mark.describe("get_order_by_id")
class TestGetOrderById:
    @pytest.mark.it("Deve retornar o pedido pelo ID")
    def test_get_order_by_id(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_order = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_order

        result = get_order_by_id(mock_db, 1)

        mock_db.query.assert_called_once_with(Order)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_order

@pytest.mark.describe("list_orders")
class TestListOrders:
    @pytest.mark.it("Deve listar pedidos com paginação")
    def test_list_orders(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_offset = mock.MagicMock()
        expected_orders = [mock.MagicMock()]

        mock_db.query.return_value = mock_query
        mock_query.offset.return_value = mock_offset
        mock_offset.limit.return_value.all.return_value = expected_orders

        result = list_orders(mock_db, skip=5, limit=20)

        mock_db.query.assert_called_once_with(Order)
        mock_query.offset.assert_called_once_with(5)
        mock_offset.limit.assert_called_once_with(20)
        mock_offset.limit.return_value.all.assert_called_once()
        assert result == expected_orders

@pytest.mark.describe("update_order")
class TestUpdateOrder:
    @pytest.mark.it("Deve atualizar o status do pedido")
    def test_update_order(self):
        mock_db = mock.MagicMock()
        mock_order = mock.MagicMock()
        mock_order_in = mock.MagicMock(status="finalizado")

        result = update_order(mock_db, mock_order, mock_order_in)

        assert mock_order.status == "finalizado"
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_order)
        assert result == mock_order

@pytest.mark.describe("delete_order")
class TestDeleteOrder:
    @pytest.mark.it("Deve remover o pedido do banco")
    def test_delete_order(self):
        mock_db = mock.MagicMock()
        mock_order = mock.MagicMock()

        delete_order(mock_db, mock_order)

        mock_db.delete.assert_called_once_with(mock_order)
        mock_db.commit.assert_called_once()