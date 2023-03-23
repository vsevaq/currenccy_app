from datetime import date

from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow.fields import Date, String


class CurrencySnapshotModelSerializer(SQLAlchemyAutoSchema):
    class Meta:
        from .model import CurrencySnapshot

        model = CurrencySnapshot


class CurrencySnapshotModelDeserializer(Schema):
    currency_code = String(allow_none=False, required=True)
    snapshot_date = Date(allow_none=True, required=False, default=date.today())


class SimplePeriodDateDeserializer(Schema):
    start_date = Date(allow_none=False, required=True, default=date.today())
    end_date = Date(allow_none=False, required=True, default=date.today())
