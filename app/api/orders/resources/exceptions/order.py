from app.schemas.base import AppHTTPException


class OrderNotFound(AppHTTPException):
    http_code = 404
    type = "OrderNotFound"
    user_message = "Заказ не найден"
    detail = "Order does not exist"


class ProductNotFound(AppHTTPException):
    http_code = 404
    type = "ProductNotFound"
    user_message = "Товар не найден"
    detail = "Product does not exist"


class NotEnoughStock(AppHTTPException):
    http_code = 409
    type = "NotEnoughStock"
    user_message = "Недостаточно товара на складе"
    detail = "Not enough stock for requested quantity"
