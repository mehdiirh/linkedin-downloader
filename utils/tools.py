import datetime
import random
import string


def now():
    """
    return current datetime as string in format '%Y-%m-%d %H:%M:%S' (UTC)
    Returns:
        str: current datetime
    """

    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def generate_unique_id(length: int = 32) -> str:
    """
    generate a unique hex ID

    Args:
        length (int): expected length of string

    Returns:
        str: hex unique id
    """

    while True:
        token = [random.choice(string.hexdigits) for _ in range(length)]
        token = "".join(token)
        token = token.lower()
        return token
