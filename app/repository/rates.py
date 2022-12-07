from app import db
from sqlalchemy import text
from app.repository.query_generator import generate_find_rate_query


def fetch_rates(origin: str, destination: str, date_from: str, date_to: str) -> list:
    """
    :param origin: originating port or region slug
    :param destination: destination port or region slug
    :param date_from: start date to query from
    :param date_to: last date to query to
    :return: List of average prices for each day from start date to end date
    """

    # generate sql query
    sql = generate_find_rate_query(origin, destination, date_from, date_to)

    # execute query and return result set
    results = db.engine.execute(text(sql))

    # convert result set to list and parse date
    prices = []
    number_of_records = 0
    for record in results.mappings().all():
        prices.append({"day": record["day"].strftime('%Y-%m-%d'), "average_price": record["average_price"]})
        if record["average_price"]:
            number_of_records += 1

    # return empty list if price does not exist for any date
    if number_of_records == 0:
        return []
    else:
        return prices

