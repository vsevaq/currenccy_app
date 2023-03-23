from app_config import supported_currency_codes


def add_currencies() -> None:
    """Fulfilling 'currency' table"""
    from api.model import Currency
    from db import database

    for code in supported_currency_codes:
        if not database.session.query(Currency).filter_by(code=code).first():
            database.session.add(Currency(code=code))
    database.session.commit()
