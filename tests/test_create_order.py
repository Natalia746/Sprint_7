import pytest
import allure

from data import DataForOrder


@allure.feature("Создание заказа /api/v1/orders")
class TestOrderCreation:
    @pytest.mark.parametrize("colors", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    @allure.title("Создание заказа с разными вариантами выбора цвета самоката")
    def test_order_creation_with_different_colors(self, colors, create_and_cancel_order):
        with allure.step(f"Тест с цветами: {colors}"):
            order_data = DataForOrder.ORDER_DATA.copy()
            order_data["color"] = colors
            track = create_and_cancel_order(order_data)
            assert track is not None, "Заказ не был успешно создан"
            allure.dynamic.description(f"Создан заказ с цветами {colors}. Track: {track}")