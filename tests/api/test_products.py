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
from app.api.products import list_products, get, create, update, delete


@pytest.mark.describe("Testes para rotas de produtos")
class TestProductRoutes:

    @pytest.mark.it("Deve listar produtos com filtros")
    @mock.patch("app.api.products.get_products", return_value=["produto1", "produto2"])
    def test_list_products(self, mock_get_products):
        mock_db = mock.MagicMock()
        result = list_products(skip=0, limit=10, category="bebidas", price=10, available=True, db=mock_db)
        mock_get_products.assert_called_once_with(mock_db, 0, 10, "bebidas", 10, True)
        assert result == ["produto1", "produto2"]

    @pytest.mark.it("Deve retornar produto por ID se existir")
    @mock.patch("app.api.products.get_product_by_id", return_value="produto")
    def test_get_product_success(self, mock_get_product_by_id):
        mock_db = mock.MagicMock()
        result = get(id=1, db=mock_db)
        mock_get_product_by_id.assert_called_once_with(mock_db, 1)
        assert result == "produto"

    @pytest.mark.it("Deve lançar 404 se produto não encontrado")
    @mock.patch("app.api.products.get_product_by_id", return_value=None)
    def test_get_product_not_found(self, mock_get_product_by_id):
        with pytest.raises(HTTPException) as exc:
            get(id=1, db=mock.MagicMock())
        assert exc.value.status_code == 404
        assert exc.value.detail == "Produto não encontrado"

    @pytest.mark.it("Deve criar produto se for admin")
    @mock.patch("app.api.products.create_product", return_value="produto_criado")
    def test_create_product_admin(self, mock_create_product):
        mock_user = mock.MagicMock(is_admin=True)
        mock_db = mock.MagicMock()
        mock_product_in = mock.MagicMock()

        result = create(product_in=mock_product_in, db=mock_db, current_user=mock_user)

        mock_create_product.assert_called_once_with(mock_db, mock_product_in)
        assert result == "produto_criado"

    @pytest.mark.it("Deve negar criação se não for admin")
    def test_create_product_not_admin(self):
        mock_user = mock.MagicMock(is_admin=False)

        with pytest.raises(HTTPException) as exc:
            create(product_in=mock.MagicMock(), db=mock.MagicMock(), current_user=mock_user)
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve atualizar produto se for admin e existir")
    @mock.patch("app.api.products.update_product", return_value="produto_atualizado")
    @mock.patch("app.api.products.get_product_by_id")
    def test_update_product_admin(self, mock_get_product, mock_update_product):
        mock_get_product.return_value = mock.MagicMock()
        mock_user = mock.MagicMock(is_admin=True)

        result = update(id=5, product_in=mock.MagicMock(), db=mock.MagicMock(), current_user=mock_user)

        assert result == "produto_atualizado"

    @pytest.mark.it("Deve negar atualização se não for admin")
    def test_update_product_not_admin(self):
        mock_user = mock.MagicMock(is_admin=False)
        with pytest.raises(HTTPException) as exc:
            update(id=5, product_in=mock.MagicMock(), db=mock.MagicMock(), current_user=mock_user)
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve lançar 404 na atualização se produto não existir")
    @mock.patch("app.api.products.get_product_by_id", return_value=None)
    def test_update_product_not_found(self, mock_get_product):
        mock_user = mock.MagicMock(is_admin=True)
        with pytest.raises(HTTPException) as exc:
            update(id=99, product_in=mock.MagicMock(), db=mock.MagicMock(), current_user=mock_user)
        assert exc.value.status_code == 404

    @pytest.mark.it("Deve excluir produto se for admin")
    @mock.patch("app.api.products.delete_product")
    @mock.patch("app.api.products.get_product_by_id")
    def test_delete_product_admin(self, mock_get_product, mock_delete_product):
        mock_get_product.return_value = mock.MagicMock()
        mock_user = mock.MagicMock(is_admin=True)
        mock_db = mock.MagicMock()

        result = delete(id=1, db=mock_db, current_user=mock_user)

        mock_delete_product.assert_called_once()
        assert result == {"detail": "Produto excluído com sucesso"}

    @pytest.mark.it("Deve negar exclusão se não for admin")
    def test_delete_product_not_admin(self):
        mock_user = mock.MagicMock(is_admin=False)
        with pytest.raises(HTTPException) as exc:
            delete(id=1, db=mock.MagicMock(), current_user=mock_user)
        assert exc.value.status_code == 403

    @pytest.mark.it("Deve lançar 404 na exclusão se produto não existir")
    @mock.patch("app.api.products.get_product_by_id", return_value=None)
    def test_delete_product_not_found(self, mock_get_product):
        mock_user = mock.MagicMock(is_admin=True)
        with pytest.raises(HTTPException) as exc:
            delete(id=1, db=mock.MagicMock(), current_user=mock_user)
        assert exc.value.status_code == 404
