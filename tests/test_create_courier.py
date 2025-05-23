
import pytest
from courier_methods import *
from generators import generate_unique_login


@allure.feature("Создание курьера /api/v1/courier")
class TestCreateCourier:
    @allure.title("Успешное создание курьера с заполнением логина, пароля и имени")
    def test_success_create_courier(self,registered_courier):

        login, password,_ = registered_courier
        response = CourierMethods.auth_courier(login, password)

        assert response.status_code == 200, "Ошибка авторизации"
        assert "id" in response.json(), "Поле 'id' отсутствует в ответе"

    @allure.title("Попытка дублирования курьера: проверка сообщения 'Этот логин уже используется'")
    def test_create_duplicate_courier(self, registered_courier):

        login, password, first_name = registered_courier

        with allure.step("Пытаемся создать второго курьера с тем же логином"):
            payload = {
                "login": login,
                "password": "any_password",
                "firstName": "any_name"
            }

            duplicate_response = CourierMethods.create_courier(payload)

            assert duplicate_response.status_code == 409, f"Ожидался 409, получен {duplicate_response.status_code}"
            assert "Этот логин уже используется" in duplicate_response.json().get("message",
                                                                                  ""), "Некорректное сообщение"

    @allure.title("Проверка создания курьера с разной длиной логина: 2,3,6,9(201) vs 1,11,12,30(400)")
    @pytest.mark.parametrize("login_length, expected_status",
                             [(2, 201),(3, 201), (6, 201), (9, 201),  # Valid cases
                              (1, 400), (11, 400), (12, 400), (30, 400)])  # Invalid cases
    def test_login_length_boundary_values(self, login_length, expected_status):

        with allure.step(f"Проверка длины логина {login_length}. Ожидаем {expected_status}"):
            # Генерируем уникальный логин с временной меткой
            base_login = generate_random_string(login_length)
            unique_login = f"{base_login}_{int(time.time() * 1000)}"

            payload = {
                "login": unique_login,
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }

            response = CourierMethods.create_courier(payload)

            if response.status_code == 409:
                pytest.skip(f"Логин {unique_login} уже существует. Требуется пересмотреть генерацию логинов.")

            assert response.status_code == expected_status, (
                f"Неверный статус код. Ожидалось {expected_status}, получено {response.status_code}"
            )

            if response.status_code == 201:
                CourierMethods.validate_success_creation(response, payload["login"], payload["password"])
            else:
                CourierMethods.validate_error_response(response, 400)

    @allure.title("Проверка обязательности полей login и password при создании курьера")
    @pytest.mark.parametrize("missing_field, test_description", [
        ("login", "Создание курьера без логина"),
        ("password", "Создание курьера без пароля"),
        ("both", "Создание курьера без логина и пароля")
    ])
    def test_missing_required_fields(self, missing_field, test_description):
        with allure.step(test_description):

            payload = {
                "login": generate_random_string(10),
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }

            if missing_field == "login":
                del payload["login"]
            elif missing_field == "password":
                del payload["password"]
            else:
                del payload["login"]
                del payload["password"]

            response = CourierMethods.create_courier(payload)

            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )

            response_body = response.json()
            assert response_body["message"] == "Недостаточно данных для создания учетной записи", (
                f"Некорректное сообщение об ошибке: {response_body.get('message')}"
            )

            assert "ok" not in response_body, "Ответ содержит неожиданное поле 'ok'"

    @allure.title("Проверка невалидных значений в логине: спецсимволы и отрицательные числа")
    @pytest.mark.parametrize("login_value, test_description", [
        ("test@user!", "Спецсимволы в логине"),
        ("-12345", "Отрицательное число в логине"),
        ("user#", "Символ решетки в логине"),
        ("$$admin$$", "Символы доллара в логине"),
        (12345, "Числовой логин"),
        (-999, "Отрицательное числовое значение"),
    ])
    def test_invalid_login_values(self, login_value, test_description):
        with allure.step(f"Тест: {test_description}"):

            base_login = str(login_value) if isinstance(login_value, int) else login_value
            unique_login = f"{base_login}_{int(time.time() * 1000)}"

            payload = {
                "login": unique_login,
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }

            response = CourierMethods.create_courier(payload)
            assert response.status_code == 400, (
                f"Ожидалось 400, получено {response.status_code}. Ответ: {response.text}"
            )

            if response.status_code == 201:
                CourierMethods.validate_success_creation(response, payload["login"], payload["password"])
            else:
                CourierMethods.validate_error_response(response, 400)

    @allure.title("Проверка невалидных значений в пароле: спецсимволы, числа и граничные случаи")
    @pytest.mark.parametrize("password_value, test_description", [
        ("pass@word!", "Спецсимволы в пароле"),
        ("-12345", "Отрицательное число как пароль"),
        ("sec#ret", "Символ решетки"),
        ("$$admin$$", "Символы доллара"),
        (12345, "Числовое значение"),
        (-999, "Отрицательное число"),
        ("   ", "Пробелы вместо пароля"),
        ("apj", "Пароль из 3 символов"),
        ("acdfg", "Пароль из 5 символов"),
        ("роли", "Пароль из русских букв"),
        ("a" * 1001, "Пароль длиннее 1000 символов")
        ])
    def test_invalid_password_values(self, password_value, test_description):
        with allure.step(f"Тест: {test_description}"):
                login = generate_unique_login()

                processed_password = (
                    str(password_value)
                    if isinstance(password_value, (int, float))
                    else password_value
                )

                payload = {
                    "login": login,
                    "password": processed_password,
                    "firstName": generate_random_string(10)
                }

                response = CourierMethods.create_courier(payload)
                assert response.status_code == 400, (
                    f"Ожидалось 400, получено {response.status_code}. Ответ: {response.text}"
                )

                if response.status_code == 201:
                    CourierMethods.validate_success_creation(response, payload["login"], payload["password"])
                else:
                    CourierMethods.validate_error_response(response, 400)