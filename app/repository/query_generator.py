from app.helper.validator import is_valid_port_code


def generate_find_rate_query(origin: str, destination: str, date_from: str, date_to: str) -> str:
    """
    :param origin: originating port or region slug
    :param destination: destination port or region slug
    :param date_from: start date to query from
    :param date_to: last date to query to
    :return: final query to be executed by the db
    """

    code_from_slug_query = "select code from public.ports where parent_slug in (select slug from regions " \
                           "where parent_slug = '{slug}' or slug = '{slug}')"

    gs_query = f"select dt::date as day, bt.average_price from " \
               f"generate_series('{date_from}', '{date_to}', INTERVAL '1 day') dt " \
               f"LEFT JOIN base_table bt on bt.day = dt"

    # check if origin is a valid port else it's a slug, assign query accordingly
    if is_valid_port_code(origin):
        orig_query = f"'{origin}'"
    else:
        orig_query = code_from_slug_query.format(slug=origin)

    # check if destination is a valid port else it's a slug, assign query accordingly
    if is_valid_port_code(destination):
        dest_query = f"'{destination}'"
    else:
        dest_query = code_from_slug_query.format(slug=destination)

    sql = "WITH base_table as (SELECT day, round(avg(price)) as average_price from public.prices " \
          "where orig_code in ({origin_query}) and dest_code in ({destination_query}) " \
          "and day between '{date_from}' and '{date_to}' GROUP BY day HAVING count(price) > 3 ORDER BY day)" \
          " {generated_seq_query}"

    # plug in appropriate parameters to build actual query string
    sql = sql.format(origin_query=orig_query,
                     destination_query=dest_query,
                     date_from=date_from,
                     date_to=date_to,
                     generated_seq_query=gs_query)

    return sql
