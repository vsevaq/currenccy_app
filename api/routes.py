from datetime import datetime, date

from flask import jsonify
from flask_smorest import Blueprint

from api.serializers import (
    CurrencySnapshotModelSerializer,
    CurrencySnapshotModelDeserializer,
    SimplePeriodDateDeserializer,
)
from .model import Currency, CurrencySnapshot


exchapi = Blueprint(
    "exchapi",
    "exchapi",
    url_prefix="/exch-api",
)


@exchapi.route(methods=["GET"], rule="/currency-rate")
@exchapi.arguments(CurrencySnapshotModelDeserializer, as_kwargs=True, location="query")
def get_external_rate(currency_code: str, snapshot_date: date):
    """
    Retrieves the currency rate by date

    Args:
        currency_code (string): 3-letteres code of some national currency
        snapshot_date (datetime): date of currency rate

    Return:
        JSON: CurrencySnapshot model serialization by CurrencySnapshotModelSerializer
            or abort

    Example: http://tld/exch-api/currency-rate
    ?currency_code=PLN
    &snapshot_date=2021-01-30
    """
    currency = CurrencySnapshot.get_external_rate(
        currency_code=currency_code, creation_date=snapshot_date
    )
    if not currency:
        return jsonify({"msg": f"No rates for date {snapshot_date}", "data": []})
    return {"msg": "Success", "data": CurrencySnapshotModelSerializer().dump(currency)}


@exchapi.route(methods=["GET"], rule="/currency-rate/history")
@exchapi.arguments(
    CurrencySnapshotModelDeserializer(only=("currency_code",)),
    as_kwargs=True,
    location="query",
)
@exchapi.arguments(SimplePeriodDateDeserializer, location="query")
def get_external_rate_history(currency_code: str, period: dict = None):
    """
    Returns the currency rate history data

    Args:
        currency_code (string): 3-letteres code of some national currency
        period(dict):
            SubArgs: start_date, end_date - periodic date objects

    Return:
        JSON: CurrencySnapshot model serialization by CurrencySnapshotModelSerializer
            or abort

    Example: https://tld/exch-api/currency-rate/history
    ?currency_code=PLN
    &start_date=2021-01-30
    &end_date=2021-01-30
    """
    currencies = Currency.get_external_rate_history(
        currency_code=currency_code, period=period
    )
    return {
        "msg": "Success",
        "data": CurrencySnapshotModelSerializer(many=True).dump(currencies),
    }
