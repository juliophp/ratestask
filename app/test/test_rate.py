from app import app


def test_invalid_date():
    client = app.test_client()
    url = "/rates?date_from=2016-01-10&date_to=2016&origin=CNSGH&destination=north_europe_main"
    response = client.get(url)
    assert response.status_code == 400


def test_missing_destination():
    client = app.test_client()
    url = "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination="
    response = client.get(url)
    assert response.status_code == 400


def test_missing_origin():
    client = app.test_client()
    url = "/rates?date_from=2016-01-10&date_to=2016&origin=&destination=north_europe_main"
    response = client.get(url)
    assert response.status_code == 400


def test_invalid_date_range():
    client = app.test_client()
    url = "/rates?date_from=2016-01-10&date_to=2016-01-01&origin=CNSGH&destination=CNSGH"
    response = client.get(url)
    assert response.status_code == 400


def test_valid_call():
    client = app.test_client()
    url = "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=north_europe_main&destination=CNSGH"
    response = client.get(url)
    assert response.status_code == 200


def test_valid_dates_between_01st_and_10thJan():
    client = app.test_client()
    url = "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
    response = client.get(url)
    print(response.get_json())
    assert response.response == 200


def test_no_record():
    client = app.test_client()
    url = "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_mainz"
    response = client.get(url)
    assert response.get_json() == '{"code": "97","message": "no record found for this date and location"}'
    assert response.response == 200

