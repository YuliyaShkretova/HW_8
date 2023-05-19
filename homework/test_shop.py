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


@pytest.fixture
def product_2():
    return Product("book_2", 200, "This is a 2nd book", 2000)


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
        # TODO Проверка добавления товара в пустую корзину
        cart.add_product(product=product, buy_count=2)
        actual_price = cart.get_total_price()
        expected_price = product.price * cart.products[product]
        assert actual_price == expected_price

    def test_add_product_add_to_ex(self, product, cart):
        # TODO Проверка добавления товара к существующему в коризне
        cart.add_product(product=product, buy_count=5)
        cart.add_product(product=product, buy_count=2)
        actual_price = cart.get_total_price()
        expected_price = product.price * cart.products[product]
        assert actual_price == expected_price

    def test_remove_product(self, product, cart):
        # TODO Проверка количества товара в корзине после удаления
        cart.add_product(product=product, buy_count=150)
        cart.remove_product(product=product, remove_count=50)
        assert cart.products == {product: 100}

    def test_remove_product_empty_qty(self, product, cart):
        # TODO Проверка пустой корзины после удаления товара без указания количества
        cart.add_product(product=product, buy_count=150)
        cart.remove_product(product=product, remove_count=None)
        assert len(cart.products) == 0

    def test_remove_product_none(self, product_2, product, cart):
        # TODO Проверка ошибки в случае попытки удаления товара, которого в корзине нет
        with pytest.raises(KeyError, match='Товар не найден в корзине'):
            cart.remove_product(product=product_2)

    def test_remove_product_more(self, product, cart):
        # TODO Проверка пустой корзины, если удаляется количество больше, чем в корзине
        cart.add_product(product=product, buy_count=150)
        cart.remove_product(product=product, remove_count=200)
        assert len(cart.products) == 0

    def test_remove_product_2nd_item_left(self, product, cart, product_2):
        # TODO Проверка количества товара в корзине после удаления
        cart.add_product(product=product, buy_count=150)
        cart.add_product(product=product_2, buy_count=150)
        cart.remove_product(product=product, remove_count=100)
        assert cart.products == {product: 50, product_2: 150}

    def test_clear(self, product, cart):
        # TODO Проверка корзины на отстутствие товара
        cart.add_product(product=product, buy_count=150)
        cart.clear()
        assert len(cart.products) == 0

    def test_clear_two_items(self, product, cart, product_2):
        # TODO Проверка корзины на отстутствие товара
        cart.add_product(product=product_2, buy_count=150)
        cart.add_product(product=product, buy_count=150)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, product, cart):
        # TODO Сравнение ожидаемой и фактической стоимости
        cart.add_product(product=product)
        expected_price = product.price
        actual_price = cart.get_total_price()
        assert actual_price == expected_price

    def test_get_total_price_two_items(self, product, product_2, cart):
        # TODO Сравнение ожидаемой и фактической стоимости
        cart.add_product(product=product)
        cart.add_product(product=product_2)
        expected_price = product.price + product_2.price
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
