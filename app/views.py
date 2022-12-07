from app import app
from flask import jsonify, request

from app.helper.validator import is_valid_date_and_range, is_valid_origin_destination
from app.repository.rates import fetch_rates


@app.route('/rates', methods=['GET'])
def get_rates():
    # extract request parameters
    args = request.args
    date_from = args.get("date_from", default="", type=str)
    date_to = args.get("date_to", default="", type=str)
    destination = args.get("destination", default="", type=str)
    origin = args.get("origin", default="", type=str)

    # validate request parameters
    is_valid_dates = is_valid_date_and_range(date_from, date_to)
    if not is_valid_dates:
        return jsonify({"code": "99", "message": "format is either invalid or date_to is earlier than date_from"}), 400
    is_valid_locations = is_valid_origin_destination(origin, destination)
    if not is_valid_locations:
        return jsonify({"code": "98", "message": "location is invalid, please check location"}), 400

    # fetch rates and return to client
    result = fetch_rates(origin, destination, date_from, date_to)

    if len(result) == 0:
        return jsonify({"code": "97", "message": "no record found for this date and location"}), 200

    return jsonify(result), 200


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"code": "96", "message": "system malfunction please contact admin"})


@app.errorhandler(404)
def internal_error(error):
    return jsonify({"code": "95", "message": "invalid request path"})
