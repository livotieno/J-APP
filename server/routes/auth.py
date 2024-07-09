from flask import Blueprint
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, abort, reqparse
from flask_jwt_extended import create_access_token, JWTManager

from models import User, db

auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api(auth_bp)

signUp_args = reqparse.RequestParser()
signUp_args.add_argument('username', type=str,
                         required=True, help='Username cannot be blank')
signUp_args.add_argument('role', type=str, required=True,
                         help='Role cannot be blank')
signUp_args.add_argument('email', type=str, required=True)
signUp_args.add_argument("password", type=str, required=True)
signUp_args.add_argument("confirmPassword", type=str)


login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, required=True)
login_args.add_argument("password", type=str, required=True)


class UserRegister(Resource):
    # *Create: POST*
    def post(self):
        data = signUp_args.parse_args()
        if data["password"] != data["confirmPassword"]:
            return abort(422, detail="Passwords do not match")

        new_user = User(username=data.username, email=data.email, role=data.role, password=bcrypt.generate_password_hash(
            data.password).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        metadata = {"username": new_user.username}
        token = create_access_token(
            identity=new_user.id, additional_claims=metadata)
        return {"detail": f"User {data.username} has been successfully created", "access token": token}


class Login(Resource):
    # *Create: POST*
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.email).first()

        if not user:
            return abort(404, detail="User does not exist")

        if not bcrypt.check_password_hash(user.password, data['password']):
            return abort(403, detail="Incorrect password")
        token = create_access_token(identity=user.id)
        return {"access_token": token, "user_id": user.id, "role": user.role, "created_at": user.created_at.isoformat()}


api.add_resource(Login, '/login')
api.add_resource(UserRegister, "/register")



# Create: POST
# Read: GET
# Update: PUT/PATCH
# Delete: DELETE