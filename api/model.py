from __future__ import annotations
from datetime import date
from operator import or_
from typing import Optional

from sqlalchemy import Column, Float, ForeignKey, Integer, Text, Date

from db import database


class Currency(database.Model):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    history = database.relationship(
        "CurrencySnapshot",
        lazy="dynamic",
        uselist=True,
        back_populates="currency",
    )

    @classmethod
    def get_external_rate_history(cls, currency_code: str, period: dict = None) -> list:
        """
        Returns the currency rate history data

        Args:
            currency_code (string): code field of Currency model
            period(dict): - periodic date objects (start_date, end_date)

        Return:
            CurrencySnapshot model list
        """
        if period:
            start_date = period["start_date"]
            end_date = period["end_date"]
            return (
                database.session.query(CurrencySnapshot)
                .join(CurrencySnapshot.currency)
                .filter(
                    Currency.code == currency_code,
                    or_(
                        CurrencySnapshot.creation_date >= start_date,
                        CurrencySnapshot.creation_date <= end_date,
                    ),
                )
                .all()
            )
        return (
            database.session.query(cls)
            .filter_by(code=currency_code)
            .first()
            .history.all()
        )


class CurrencySnapshot(database.Model):
    __tablename__ = "currency_snapshot"

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    to_usd_price = Column(Float(), nullable=False)
    creation_date = Column(Date, nullable=False, default=date.today())
    currency = database.relationship(
        "Currency", back_populates="history", uselist=False
    )

    @classmethod
    def get_external_rate(cls, currency_code: str, creation_date: date) -> Optional:
        """
        Returns the currency rate history data

        Args:
            currency_code (string): code field of Currency model
            creation_date(date): - date of rate into database adding

        Return:
            CurrencySnapshot model instance
        """
        return (
            database.session.query(cls)
            .join(cls.currency)
            .filter(cls.creation_date == creation_date, Currency.code == currency_code)
            .order_by(cls.creation_date.desc())
            .first()
        )
