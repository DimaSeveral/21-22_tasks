from exceptions import InvalidNumberError, UnsupportedOperationError, NegativeResultError

def validate_digits(digits: list[int]) -> None:
    if not all(isinstance(d, int) and 0 <= d <= 9 for d in digits):
        raise InvalidNumberError("Все цифры должны быть от 0 до 9")

def digits_to_int(digits: list[int]) -> int:
    validate_digits(digits)
    return int(''.join(map(str, digits)))

def int_to_digits(n: int) -> list[int]:
    if n < 0:
        raise ValueError("Ожидалось неотрицательное число")
    return [int(d) for d in str(n)]

def process_big_numbers(a: list[int], b: list[int], operation: str) -> list[int]:
    num_a = digits_to_int(a)
    num_b = digits_to_int(b)

    if operation == 'add':
        result = num_a + num_b
        return int_to_digits(result)
    elif operation == 'sub':
        result = num_a - num_b
        if result < 0:
            raise NegativeResultError("Результат отрицателен и не поддерживается.")
        return int_to_digits(result)
    else:
        raise UnsupportedOperationError("Неверная операция. Доступно: add, sub")