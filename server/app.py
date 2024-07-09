import os


from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from datetime import timedelta

from models import db, TokenBlocklist

from routes.auth import auth_bp, jwt
from routes.user_bp import user_bp, bcrypt
from routes.entry_bp import entry_bp
from routes.category_bp import category_bp


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma = Marshmallow(app)
    migrate = Migrate(app, db)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist).filter_by(jti=jti).first()
        return token is not None
    
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(entry_bp)
    app.register_blueprint(category_bp)

    CORS(app, resources={r"*": {"origins": "*"}})
    return app


app = create_app()