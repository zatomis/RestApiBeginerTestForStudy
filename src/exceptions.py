from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Такой объект уже существует"


class EmptyValueException(NabronirovalException):
    detail = "Данные являются пустыми"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TableNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Столик не найден"


class ReservationsNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Нет такой брони"


class TableIsNotAvailableHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Cтолик не доступен в это время"
