import math


def multiples(limit: int) -> int:
    """This function finds the sum of all the natural numbers that are multiples of 3 or 5 below limit,
    that is passed as an argument
    Args:
    limit (int) - upper value (including itself) for which multiples will be searched"""
    # finding the quantity of multiples for each number
    # num_15 is needed to remove duplicates - numbers that are multiples for both 3 and 5
    num_3 = math.ceil(limit / 3)
    num_5 = math.ceil(limit / 5)
    num_15 = math.ceil(limit / 15)

    # calculating sum of numbers for each multiple according to arithmetic progression formula
    sum_3 = ((3 * (num_3 - 1)) * num_3) / 2
    sum_5 = ((5 * (num_5 - 1)) * num_5) / 2
    sum_15 = ((15 * (num_15 - 1)) * num_15) / 2

    return int(sum_3 + sum_5 - sum_15)


if __name__ == "__main__":
    limit = 100000000
    print(multiples(limit=limit))
