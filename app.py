import os
import config
from flask import Flask
from models.base_model import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'garage_sale_web')

app = Flask('GARAGE_SALE', root_path=web_dir)

app.config['JWT_SECRET_KEY'] = 'garage_sale_jwt_key'  # Change this!
jwt = JWTManager(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
