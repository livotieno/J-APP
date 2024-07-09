from flask import Blueprint, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import datetime

from models import User, db


from serializers import UserSchema

user_bp = Blueprint('user_bp', __name__)
ma = Marshmallow(user_bp)
bcrypt = Bcrypt()
api = Api(user_bp)

post_args = reqparse.RequestParser()
post_args.add_argument('id', type=str, required=True, help='ID is required')
post_args.add_argument('username', type=str, required=True,
                       help='Username is required')
post_args.add_argument('password', type=str, required=True,
                       help='Password is required')
post_args.add_argument('created_at', type=str,
                       required=True, help='Created_at is required')
post_args.add_argument('updated_at', type=str,
                       required=True, help='Updated_at is required')

patch_args = reqparse.RequestParser()
patch_args.add_argument('username', type=str)
patch_args.add_argument('password', type=str)
patch_args.add_argument('created_at', type=str)
patch_args.add_argument('updated_at', type=str)

userschema = UserSchema(many=True)
userschema_single = UserSchema()

class Users(Resource):
    def get(self):
        users = User.query.all()
        result = userschema.dump(users, many=True)
        return jsonify(result)

    def post(self):
        data = post_args.parse_args()

        user = User.query.filter_by(id=data['id']).first()
        if not user:
            abort(409, detail="User with the same id already exists")

        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S')
        updated_at = datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%S')

        hashed_password = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        new_user = User(username=data['username'], id=data['id'], password=hashed_password,
                        role=data['role'], created_at=created_at, updated_at=updated_at)
        db.session.add(new_user)
        db.session.commit()

        result = userschema_single.dump(new_user)
        return result, 201


class UserById(Resource):
    def get(self, id):
        single_user = User.query.get(id)
        if not single_user:
            abort(404, detail=f'User with id {id} does not exist')

        result = userschema_single.dump(single_user)
        return jsonify(result)
        # Update: PUT/PATCH
    def patch(self, id):
        single_user = User.query.get(id)
        if not single_user:
            abort(404, detail=f'User with id {id} does not exist')

        data = patch_args.parse_args()

        if data['created_at']:
            created_at = datetime.strptime(
                data['created_at'], '%Y-%m-%dT%H:%M:%S')
            setattr(single_user, 'created_at', created_at)

        for key, value in data.items():
            if key == 'created_at':
                continue
            if value is not None:
                setattr(single_user, key, value)
        db.session.commit()

        result = userschema_single.dump(single_user)
        return jsonify(result)

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, detail=f'User with id {id} does not exist')

        db.session.delete(user)
        db.session.commit()
        return f'User with {id=} has been successfully deleted.', 204


api.add_resource(Users, '/users')
api.add_resource(UserById, '/user/<int:id>')


# Create: POST
# Read: GET
# Update: PUT/PATCH
# Delete: DELETE