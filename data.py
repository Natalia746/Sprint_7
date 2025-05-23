class Url:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'
    CREATE_COURIER = '/api/v1/courier'
    LOGIN_COURIER = '/api/v1/courier/login'
    DELETE_COURIER = '/api/v1/courier/{courier_id}'

class DataForAuth:
    PAYLOAD = {
    "login": "lopylopy",
    "password": "1234",
    "firstName": "ghfd"
}
    TEST_PAYLOAD = PAYLOAD.copy()


