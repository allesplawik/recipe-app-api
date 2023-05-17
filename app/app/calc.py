def add(x: int, y: int) -> int:
    return x + y


def even_numbers(numbers: list[int]) -> list[int]:
    return [number for number in numbers if number % 2 == 0]
