import re


def check_ip(ip_address: str | int) -> bool:
    """This function validates the given ip address and returns True if it's valid IPv4, otherwise False
    Args:
    ip_adress (str, int) - piece of data that will be validated if it's valid ip address
    """

    # checking if given data matches the common pattern characteristic of an ip_address
    ip_address_pattern_match = re.match(
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str(ip_address)
    )
    if not bool(ip_address_pattern_match):
        return False
    # checking that number of bytes in each slot is less than 256
    ip_address_bytes = [int(bytes) < 256 for bytes in ip_address.split(".")]

    if not all(ip_address_bytes):
        return False

    return True


if __name__ == "__main__":
    assert check_ip("") is False
    assert check_ip("192.168.0.1") is True
    assert check_ip("0.0.0.1") is True
    assert check_ip("10.100.500.32") is False
    assert check_ip(700) is False
    # there was a typo in this assertion in the task - '127.0.1' was supposed to be True though it is not
    # checked via ipadress.ip_address() - ValueError: '127.0.1' does not appear to be an IPv4 or IPv6 address
    assert check_ip("127.0.0.1") is True
