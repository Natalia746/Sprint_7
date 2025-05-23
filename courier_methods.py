import allure
import requests
from data import Url
from generators import *


class CourierMethods:
    @staticmethod
    @allure.step("Регистрация курьера и возврат логина, пароля и имени")
    def register_new_courier_and_return_login_password():
        payload = {
            "login": generate_unique_login(),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(
            f"{Url.BASE_URL}{Url.CREATE_COURIER}",
            json=payload
        )

        if response.status_code != 201:
            raise Exception(f"Ошибка регистрации: {response.text}")

        return [payload["login"], payload["password"], payload["firstName"]]

    @staticmethod
    @allure.step("Авторизация курьера и возврат ID")
    def auth_courier(login, password):
        response = requests.post(
            f"{Url.BASE_URL}{Url.LOGIN_COURIER}",
            json={"login": login, "password": password}
        )
        return response

    @staticmethod
    @allure.step("Удаление курьера по ID")
    def delete_courier(courier_id):
        response = requests.delete(
            f"{Url.BASE_URL}{Url.DELETE_COURIER.format(courier_id=courier_id)}"
        )
        if response.status_code != 200:
            raise Exception(f"Ошибка удаления: {response.text}")

    @staticmethod
    @allure.step("Создание курьера (для негативных тестов) без генерации данных")
    def create_courier(payload):
        return requests.post(
            f"{Url.BASE_URL}{Url.CREATE_COURIER}",
            json=payload
        )

    @staticmethod
    @allure.step("Проверка успешного создания курьера и удаление тестовых данных")
    def validate_success_creation(response, login, password):
        response_body = response.json()
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "ok" in response_body and response_body["ok"] is True, "Некорректное тело успешного ответа"

        auth_response = CourierMethods.auth_courier(login, password)
        courier_id = auth_response.json()["id"]
        CourierMethods.delete_courier(courier_id)

    @staticmethod
    @allure.step("Проверка сообщения об ошибке")
    def validate_error_response(response, expected_status):
        response_body = response.json()
        assert response.status_code == expected_status, f"Ожидался статус {expected_status}, получен {response.status_code}"
        assert "message" in response_body, "Отсутствует сообщение об ошибке"

