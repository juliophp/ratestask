from datetime import datetime


def is_valid_date_and_range(from_date: str, to_date: str) -> bool:
    """
    :param from_date: start date to query from
    :param to_date: last date to query to
    :return: Boolean to evaluate if date format is valid and are in proper order
    """
    try:
        from_date = get_date_from_string(from_date)
        to_date = get_date_from_string(to_date)
        return from_date <= to_date
    except ValueError:
        return False


def is_valid_origin_destination(origin: str, destination: str) -> bool:
    """
    :param origin: originating port or region slug
    :param destination: destination port or region slug
    :return: Boolean value to validate both origin and destination
    """
    return len(origin) >= 5 and len(destination) >= 5


def is_valid_port_code(code: str) -> bool:
    """
    :param code: port code
    :return: Boolean to validate if the port code is valid
    """
    return len(code) == 5 and code.isupper()


def get_date_from_string(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d')
