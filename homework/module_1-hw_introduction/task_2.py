def min_max(numbers: list) -> tuple[int, int]:
    """This function takes a list as an argument and converts its elements
    to integers, then finds maximum and minimum value.
    Args:
    numbers (list) - list of the values, which will be converted into integers if possible
    """

    converted_numbers = []
    if not numbers:
        return "Please input non-empty list"
    for number in numbers:
        try:
            converted_numbers.append(int(number))
        except (ValueError, TypeError):
            pass
    return min(converted_numbers), max(converted_numbers)


if __name__ == "__main__":
    numbers = [1, 2, "0", "300", -2.5, "Dog", True, "0o1256", None]
    print(min_max(numbers=numbers))
