from datetime import date

import requests


def get_and_save_currency_rates() -> None:
    from app_config import (
        base_currency,
        supported_currencies_string,
        external_api_key,
        supported_currency_codes,
    )
    from db import database
    from api.model import CurrencySnapshot, Currency

    response = requests.get(
        f"https://api.apilayer.com/exchangerates_data/latest"
        f"?&base={base_currency}"
        f"&symbols={supported_currencies_string}",
        headers={"apikey": external_api_key},
    )
    data = response.json()

    for code in supported_currency_codes:
        currency = database.session.query(Currency).filter_by(code=code).one_or_none()
        if currency:
            database.session.add(
                CurrencySnapshot(
                    currency_id=currency.id,
                    to_usd_price=data.get("rates", {}).get(code, 0.0),
                    creation_date=date.today(),
                )
            )
    database.session.commit()


# get_and_save_currency_rates()
