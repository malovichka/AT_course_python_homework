def min_max(numbers: list) -> int:
    """This function takes a list as an argument and converts its elements
    to integers, then finds maximum and minimum value"""

    converted_numbers = []
    for number in numbers:
        try:
            converted_numbers.append(int(number))
        except (ValueError, TypeError):
            pass
    return min(converted_numbers), max(converted_numbers)


if __name__ == "__main__":
    numbers = [1, 2, "0", "300", -2.5, "Dog", True, "0o1256", None]
    print(min_max(numbers))
