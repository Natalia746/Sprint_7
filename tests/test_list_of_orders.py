import allure
import requests

from courier_methods import CourierMethods
from data import *
from order_methods import OrderMethods

@allure.feature("Получение списка заказов GET '/api/v1/orders'")
class TestOrderList:
    @allure.title("Проверка наличия списка заказов в ответе без courierId")
    def test_order_list_response(self):
        response = OrderMethods.get_order_list()
        OrderMethods.validate_order_list_response(response)

    @allure.title("Проверка наличия списка заказов в ответе с привязкой к courierId")
    def test_courier_order_flow(self, registered_courier, created_order):
        login, password, _ = registered_courier
        order_id = created_order  # ID из фикстуры

        with allure.step("Авторизация курьера"):
            auth_response = CourierMethods.auth_courier(login, password)
            assert auth_response.status_code == 200, "Ошибка авторизации"
            courier_id = auth_response.json()["id"]

        with allure.step("Принятие заказа"):
            accept_response = OrderMethods.accept_order(order_id, courier_id)
            assert accept_response.status_code == 200, "Ошибка принятия заказа"
            assert accept_response.json().get("ok") is True

        with allure.step("Проверка списка заказов"):
            response = OrderMethods.get_courier_orders(courier_id)
            orders = response.json().get("orders", [])
            assert any(
                order["id"] == order_id and
                order["courierId"] == courier_id
                for order in orders
            ), "Заказ не привязан"

    @allure.title("Проверка ошибки при получении списка заказов курьера с несуществующим ID")
    def test_accept_order_with_invalid_courier_id(self, created_order):
        order_id = created_order  # ID из фикстуры
        invalid_courier_id = 999999  # Несуществующий ID

        with allure.step("Попытка принять заказ"):
            response = OrderMethods.accept_order(order_id, invalid_courier_id)

        with allure.step("Проверка ответа"):
            assert response.status_code == 404, "Ожидался статус 404"
            assert "Курьера с таким id не существует" in response.text