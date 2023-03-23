import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from flask_marshmallow import Marshmallow
from flask_smorest import Api

from app_config import pg_user, pg_password, pg_url, pg_database

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{pg_user}:{pg_password}@{pg_url}/{pg_database}"
app.config["SQLALCHEMY_ECHO"] = True
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["API_TITLE"] = "EXCHANGE API"
app.config["API_VERSION"] = "TEST"

# initing apscheduler
scheduler = BackgroundScheduler()
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def start_app() -> Flask:
    """Entire application starting function"""
    ma = Marshmallow()
    ma.init_app(app)

    with app.app_context():
        from db import database

        database.create_all()

    # adding 'exchapi' blueprint for executing API-endpoints
    app_api = Api(app)
    from api.routes import exchapi

    app_api.register_blueprint(exchapi)

    from utils.tasks import get_and_save_currency_rates
    with app.app_context():
        from api import add_currencies
        # fulfill database
        add_currencies()
        get_and_save_currency_rates()

        # adding schedular task
        scheduler.add_job(func=get_and_save_currency_rates, trigger="cron", hour="01")

    return app
