def fizzbuzz() -> None:
    """This function displays numbers from 1 to 100.
    If the number is a multiple of 3, word 'Fizz' is displayed instead,
    if the number is a multiple of 5 - the word 'Buzz'.
    If the number is a multiple of both 3 and 5, then 'FizzBuzz' is displayed"""

    for i in range(1, 101):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0 and i % 5 != 0:
            print("Fizz")
        elif i % 3 != 0 and i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == "__main__":
    fizzbuzz()
