import pytest
from unittest import mock
from app.crud.products import Product, get_product_by_id, get_products, create_product, update_product, delete_product


@pytest.mark.describe("get_product_by_id")
class TestGetProductById:
    @pytest.mark.it("Deve retornar produto pelo ID")
    def test_get_product_by_id(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filter = mock.MagicMock()
        expected_product = mock.MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_product

        result = get_product_by_id(mock_db, 1)

        mock_db.query.assert_called_once_with(Product)
        mock_query.filter.assert_called_once()
        mock_filter.first.assert_called_once()
        assert result == expected_product


@pytest.mark.describe("get_products")
class TestGetProducts:
    @pytest.mark.it("Deve listar produtos com filtros e paginação")
    def test_get_products_with_filters(self):
        mock_db = mock.MagicMock()
        mock_query = mock.MagicMock()
        mock_filtered = mock.MagicMock()
        expected_products = [mock.MagicMock()]

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filtered
        mock_filtered.filter.return_value = mock_filtered  # encadeamento
        mock_filtered.offset.return_value.limit.return_value.all.return_value = expected_products

        result = get_products(mock_db, skip=0, limit=10, category="livros", price=100.0, available=True)

        mock_db.query.assert_called_once_with(Product)
        assert result == expected_products


@pytest.mark.describe("create_product")
class TestCreateProduct:
    @pytest.mark.it("Deve criar um novo produto")
    def test_create_product(self):
        mock_db = mock.MagicMock()
        mock_product_data = mock.MagicMock()
        mock_product_data.model_dump.return_value = {
            "name": "Livro",
            "sale_price": 29.9,
            "section": "livros",
            "is_available": True
        }

        mock_product = mock.MagicMock()
        with mock.patch("app.crud.products.Product", return_value=mock_product):
            result = create_product(mock_db, mock_product_data)

        mock_db.add.assert_called_once_with(mock_product)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_product)
        assert result == mock_product


@pytest.mark.describe("update_product")
class TestUpdateProduct:
    @pytest.mark.it("Deve atualizar os campos de um produto existente")
    def test_update_product(self):
        mock_db = mock.MagicMock()
        mock_product = mock.MagicMock()
        mock_update_data = mock.MagicMock()
        mock_update_data.model_dump.return_value = {"sale_price": 19.9, "is_available": False}

        result = update_product(mock_db, mock_product, mock_update_data)

        assert mock_product.sale_price == 19.9
        assert mock_product.is_available is False
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_product)
        assert result == mock_product


@pytest.mark.describe("delete_product")
class TestDeleteProduct:
    @pytest.mark.it("Deve remover o produto do banco")
    def test_delete_product(self):
        mock_db = mock.MagicMock()
        mock_product = mock.MagicMock()

        delete_product(mock_db, mock_product)

        mock_db.delete.assert_called_once_with(mock_product)
        mock_db.commit.assert_called_once()