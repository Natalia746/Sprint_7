
import allure
import pytest
from courier_methods import CourierMethods


@pytest.fixture
@allure.title("Создание курьера и удаление курьера после теста")
def registered_courier():
    # Регистрация курьера и получение ВСЕХ данных
    courier_data = CourierMethods.register_new_courier_and_return_login_password()
    login, password, first_name = courier_data  # Распаковываем все 3 значения

    yield login, password, first_name # Возвращаем только логин и пароль

    # Удаление курьера после теста
    response = CourierMethods.auth_courier(login, password)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        CourierMethods.delete_courier(courier_id)