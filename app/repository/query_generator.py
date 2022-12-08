from app.helper.validator import is_valid_port_code


def generate_find_rate_query(origin: str, destination: str, date_from: str, date_to: str) -> str:
    """
    :param origin: originating port or region slug
    :param destination: destination port or region slug
    :param date_from: start date to query from
    :param date_to: last date to query to
    :return: final query to be executed by the db
    """

    sql = "WITH RECURSIVE children AS (SELECT r.slug, r.parent_slug, r.slug as heirarchy FROM regions r " \
             "WHERE r.parent_slug is null UNION ALL SELECT  rr.slug, rr.parent_slug, " \
             "rr.slug || ', ' || d.heirarchy FROM regions rr INNER JOIN children d ON d.slug = rr.parent_slug), " \
             "slugs AS (SELECT * From children), ports AS (SELECT * from public.ports p join slugs s on " \
             "p.parent_slug = s.slug), average_prices AS (SELECT day, round(avg(price)) as average_price " \
             "from public.prices where orig_code in ({origin_query}) and dest_code in " \
             "({destination_query}) and day between '{date_from}' and '{date_to}' GROUP BY day " \
             "HAVING count(price) > 3 ORDER BY day)," \
             "base_table as (select * from average_prices) select dt::date as day, bt.average_price " \
             "from generate_series('{date_from}', '{date_to}', INTERVAL '1 day') " \
             "dt LEFT JOIN base_table bt on bt.day = dt"

    ports_query = "SELECT code from ports where heirarchy like '%{slug}%'"

    # check if origin is a valid port else it's a slug, assign query accordingly
    if is_valid_port_code(origin):
        orig_query = f"'{origin}'"
    else:
        orig_query = ports_query.format(slug=origin)

    # check if destination is a valid port else it's a slug, assign query accordingly
    if is_valid_port_code(destination):
        dest_query = f"'{destination}'"
    else:
        dest_query = ports_query.format(slug=destination)

    # plug in appropriate parameters to build actual query string
    sql = sql.format(origin_query=orig_query,
                     destination_query=dest_query,
                     date_from=date_from,
                     date_to=date_to)

    return sql
