import allure
import requests

from data import Url


class OrderMethods:
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(order_data):
        return requests.post(
            f"{Url.BASE_URL}{Url.CREATE_ORDER}",
            json=order_data
        )

    @staticmethod
    @allure.step("Проверка успешного создания заказа, тело ответа содержит track")
    def validate_order_creation(response):
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "Отсутствует поле track в ответе"

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_order_list():
        return requests.get(f"{Url.BASE_URL}{Url.CREATE_ORDER}")

    @staticmethod
    @allure.step("Проверка успешного получения списка заказов")
    def validate_order_list_response(response):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_json = response.json()
        assert "orders" in response_json, "Ключ 'orders' отсутствует в ответе"
        assert isinstance(response_json["orders"], list), "Поле 'orders' не является списком"

    @staticmethod
    @allure.step("Получение списка заказов курьера")
    def get_courier_orders(courier_id):
        return requests.get(
            f"{Url.BASE_URL}{Url.CREATE_ORDER}",
            params={"courierId": courier_id}
        )

    @staticmethod
    @allure.step("Принятие заказа курьером")
    def accept_order(order_id, courier_id):
        return requests.put(
            f"{Url.BASE_URL}{Url.ACCEPT_ORDER.format(
                order_id=order_id,
                courier_id=courier_id
            )}"
        )

    @staticmethod
    @allure.step("Получение track заказа")
    def get_track (track):
        return requests.get(
            f"{Url.BASE_URL}{Url.GET_ORDER_BY_NUMBER.format(track=track)}"
        )

    @staticmethod
    @allure.step("Отмена созданного заказа")
    def cancel_order(track):
        return requests.put(f"{Url.BASE_URL}{Url.CANCEL_ORDER}")