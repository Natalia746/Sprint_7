from datetime import datetime


class Url:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'
    CREATE_COURIER = '/api/v1/courier'
    LOGIN_COURIER = '/api/v1/courier/login'
    DELETE_COURIER = '/api/v1/courier/{courier_id}'
    CREATE_ORDER = '/api/v1/orders'
    ACCEPT_ORDER = '/api/v1/orders/accept/{order_id}?courierId={courier_id}'
    GET_ORDER_BY_NUMBER = '/api/v1/orders/track?t={track}'
    CANCEL_ORDER = '/api/v1/orders/cancel?track={track}'


class DataForAuth:
    PAYLOAD = {
    "login": "lopylopy",
    "password": "1234",
    "firstName": "ghfd"
}
    TEST_PAYLOAD = PAYLOAD.copy()

class DataForOrder:
    ORDER_DATA = {
        "firstName": "Serg",
        "lastName": "Uchiha",
        "address": "Ugizy, 142 apt.",
        "metroStation": 8,
        "phone": "+7 800 355 35 35",
        "rentTime": 2,
        "deliveryDate": datetime.now().strftime("%Y-%m-%d"),
        "comment": "Jmn bkdk"
    }


