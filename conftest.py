
import allure
import pytest
import requests

from courier_methods import CourierMethods
from data import *
from order_methods import OrderMethods


@pytest.fixture
@allure.title("Создание курьера и удаление курьера после теста")
def registered_courier():
    courier_data = CourierMethods.register_new_courier_and_return_login_password()
    login, password, first_name = courier_data  # Распаковываем все 3 значения

    yield login, password, first_name # Возвращаем только логин и пароль

    response = CourierMethods.auth_courier(login, password)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        CourierMethods.delete_courier(courier_id)


@pytest.fixture
@allure.title("Создание заказа, получение ID заказа через track, отмена заказа после теста")
def created_order():

    order_response = OrderMethods.create_order(DataForOrder.ORDER_DATA)
    OrderMethods.validate_order_creation(order_response)
    track = order_response.json()["track"]

    # Получение ID заказа
    track_response = OrderMethods.get_track(track)
    assert track_response.status_code == 200, "Ошибка получения заказа"
    order_id = track_response.json()["order"]["id"]

    yield order_id  # Возвращаем ID заказа

    # Очистка: отмена заказа
    OrderMethods.cancel_order(track)


class OrderMethod:
    @classmethod
    def create_order(cls, order_data):
        pass


@pytest.fixture
@allure.title("Создание и отмена заказа")
def create_and_cancel_order():
    tracks = []

    def _create_order(order_payload):
        response = OrderMethods.create_order(order_payload)
        OrderMethods.validate_order_creation(response)

        track = response.json()["track"]
        tracks.append(track)
        return track

    yield _create_order

    # Отмена всех созданных заказов после теста
    with allure.step("Отмена созданных заказов"):
        for track in tracks:
            OrderMethods.cancel_order(track)


@pytest.fixture
def order_data():
    return DataForOrder.ORDER_DATA.copy()