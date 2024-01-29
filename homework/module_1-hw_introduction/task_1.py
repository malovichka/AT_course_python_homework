def fizzbuzz(top_value: int) -> None:
    """This function displays numbers from 1 to given top value incl.
    If the number is a multiple of 3, word 'Fizz' is displayed instead,
    if the number is a multiple of 5 - the word 'Buzz'.
    If the number is a multiple of both 3 and 5, then 'FizzBuzz' is displayed
    Args:
    top_value (int) - upper value (including itself) for which FizzBuzz will be displayed, including
    """

    for i in range(1, top_value + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == "__main__":
    fizzbuzz(top_value=100)
