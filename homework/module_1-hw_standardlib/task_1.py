def list_filtering_with_for_loop(unfiltered: list) -> list[int]:
    """This function filters only integers USING FOR LOOP from given list and returns results in new list
    Args:
    unfiltered (list) - list elements of various data types"""
    filtered = []
    for i in unfiltered:
        if isinstance(i, int):
            filtered.append(i)

    return filtered


def list_filtering_with_list_comprehensions(unfiltered: list) -> list[int]:
    """This function filters only integers USING LIST COMPREHENSIONS from given list and returns results in new list
    Args:
    unfiltered (list) - list elements of various data types"""

    return [i for i in unfiltered if isinstance(i, int)]


def list_filtering_with_filter_and_lambda(unfiltered: list) -> list[int]:
    """This function filters only integers USING FILTER() AND LAMBDA from given list and returns results in new list
    Args:
    unfiltered (list) - list elements of various data types"""

    return list(filter(lambda i: isinstance(i, int), unfiltered))


if __name__ == "__main__":
    unfiltered = [1, 2, "3", 4, None, 10, 33, "Python", -37.5]

    print(list_filtering_with_for_loop(unfiltered))
    print(list_filtering_with_list_comprehensions(unfiltered))
    print(list_filtering_with_filter_and_lambda(unfiltered))

    assert list_filtering_with_for_loop([1, 2, "a", "b"]) == [1, 2]
    assert list_filtering_with_for_loop([1, "a", "b", 0, 15]) == [1, 0, 15]
    assert list_filtering_with_for_loop([1, 2, "aasf", "1", "123", 123]) == [1, 2, 123]

    assert list_filtering_with_list_comprehensions([1, 2, "a", "b"]) == [1, 2]
    assert list_filtering_with_list_comprehensions([1, "a", "b", 0, 15]) == [1, 0, 15]
    assert list_filtering_with_list_comprehensions([1, 2, "aasf", "1", "123", 123]) == [
        1,
        2,
        123,
    ]

    assert list_filtering_with_filter_and_lambda([1, 2, "a", "b"]) == [1, 2]
    assert list_filtering_with_filter_and_lambda([1, "a", "b", 0, 15]) == [1, 0, 15]
    assert list_filtering_with_filter_and_lambda([1, 2, "aasf", "1", "123", 123]) == [
        1,
        2,
        123,
    ]
