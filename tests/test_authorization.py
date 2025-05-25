import pytest

from data import *
import allure
from courier_methods import CourierMethods


@allure.feature("Авторизация курьера /api/v1/courier/login")
class TestAuthorization:

    @allure.title("Проверка успешной авторизации ранее зарегистрированного курьера с возвращением id в теле ответа")
    def test_success_authorization_registered_courier(self):

        login = DataForAuth.PAYLOAD["login"]
        password = DataForAuth.PAYLOAD["password"]

        response = CourierMethods.auth_courier(login, password)

        assert response.status_code == 200, "Ошибка авторизации"
        assert "id" in response.json(), "Поле 'id' отсутствует в ответе"

    @allure.title("Проверка авторизации при использовании неверных учетных данных")
    @pytest.mark.parametrize("login, password, expected_status, expected_message", [
        # Неверный логин + верный пароль
        ("lopylop", DataForAuth.PAYLOAD["password"], 404, "Учетная запись не найдена"),
        # Верный логин + неверный пароль
        (DataForAuth.PAYLOAD["login"], "1245", 404, "Учетная запись не найдена"),
        # Отсутствие логина
        (None, DataForAuth.PAYLOAD["password"], 400, "Недостаточно данных для входа"),
        # Отсутствие пароля
        (DataForAuth.PAYLOAD["login"], None, 400, "Недостаточно данных для входа")
    ])
    def test_invalid_credentials_authorization(self, login, password, expected_status, expected_message):
        with allure.step(f"Тест: {expected_message} (status {expected_status})"):
            response = CourierMethods.auth_courier(login, password)

            assert response.status_code == expected_status, (
                f"Ожидался {expected_status}, получен {response.status_code}. Ответ: {response.text}"
            )

            response_body = response.json()
            assert response_body.get("message") == expected_message, (
                f"Ожидалось: '{expected_message}', получено: '{response_body.get('message')}'"
            )

