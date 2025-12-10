class AppException(Exception): #общий корень для всех ошибок
    """Базовое исключение приложения"""
    pass

class InvalidInputError(AppException): 
    """Ошибка некорректного пользовательского ввода"""
    pass

class InvalidNumberError(InvalidInputError):
    """Ошибка при вводе недопустимого 'большого числа'"""
    pass

class UnsupportedOperationError(AppException):
    """Операция не поддерживается"""
    pass

class NegativeResultError(AppException):
    """Результат отрицателен и не поддерживается"""
    pass