import time

def generate_credentials() -> tuple[str, str]:
    """Function generates unique username and password for new user registration"""
    username = "user" + str(int(time.time()))
    password = "password" + str(int(time.time()))
    return username, password

