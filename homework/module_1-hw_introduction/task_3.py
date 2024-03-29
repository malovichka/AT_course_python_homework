import string


def letters_count(text: str) -> str:
    """This function counts how many times word 'Python' is used in the given text,
    and finds the letter that is used most often. Case is ignored, as well as
    punctuation marks, special characters, spaces and newlines
    Args:
    text (str) - text in which function will search for the letter with highest occurance
    """

    most_often_count = 0
    most_often_letter = ""
    text_lower = text.lower()
    for letter in string.ascii_lowercase:
        letter_count = text_lower.count(letter)
        if letter_count > most_often_count:
            most_often_count = letter_count
            most_often_letter = letter
    return most_often_letter


def python_count(text: str) -> int:
    """This function counts how many times word 'Python' is used in the given text
    Args:
    text (str) - text in which function will count non-overlapping appearance of word 'python'
    """

    return text.lower().count("python")


if __name__ == "__main__":
    text = """
    Python is an interpreted high-level programming language for 
    general-purpose programming. Created by Guido van Rossum and first released 
    in 1991, Python has a design philosophy that emphasizes code readability, 
    notably using significant whitespace. It provides constructs that enable 
    clear programming on both small and large scales. In July 2018, the creator 
    Guido Rossum stepped down as the leader in the language community after 30 
    years. Python features a dynamic type system and automatic memory management. 
    It supports multiple programming paradigms, including object-oriented, imperative, 
    functional and procedural, and has a large and comprehensive standard library.
    Python interpreters are available for many operating systems. CPython, the reference 
    implementation of Python, is open source software and has a community-based 
    development model, as do nearly all of Python's other implementations. Python 
    and CPython are managed by the non-profit Python Software Foundation.
    """
    print(letters_count(text=text), python_count(text=text))
