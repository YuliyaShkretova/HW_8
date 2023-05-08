"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from .models import Cart, Product


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(0) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(1000)
        assert product.quantity == 0

    def test_product_buy_sec(self, product):
        # TODO напишите проверки на метод buy
        product.buy(90)
        assert product.quantity == 910

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError, match='Продукта недостаточно на складе'):
            product.buy(1100)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, product, cart):
        # TODO Проверка наличия товара в корзине
        cart.add_product(product=product, buy_count=2)
        assert cart.products[product]

    def test_remove_product(self, product, cart):
        # TODO Проверка количества товара в корзине после удаления
        cart.add_product(product=product, buy_count=150)
        cart.remove_product(product=product, remove_count=50)
        assert cart.products[product]

    def test_clear(self, product, cart):
        # TODO Проверка корзины на отстутствие товара
        cart.add_product(product=product, buy_count=150)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, product, cart):
        # TODO Сравнение ожидаемой и фактической стоимости
        cart.add_product(product=product)
        expected_price = product.price
        actual_price = cart.get_total_price()
        assert actual_price == expected_price

    def test_buy_no_qty(self, cart, product):
        # TODO Проверка вызова ошибки, если товара недостаточно
        cart.add_product(product=product, buy_count=5000)
        with pytest.raises(ValueError, match='Продукта недостаточно на складе'):
            cart.buy()

    def test_buy_self_clear(self, cart, product):
        # TODO проверка опустошения корзины после успешной покупки
        cart.add_product(product=product, buy_count=10)
        cart.buy()
        assert len(cart.products) == 0
