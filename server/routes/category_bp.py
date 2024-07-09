from flask import Blueprint, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_marshmallow import Marshmallow
from schemas import category_schema_single

from models import Category, db

from serializers import CategorySchema

category_bp = Blueprint('category_bp', __name__)
ma = Marshmallow(category_bp)
api = Api(category_bp)

post_args = reqparse.RequestParser()
post_args.add_argument('unit_id', type=str,
                       help='unit_id is required')
post_args.add_argument('name', type=str,
                       required=True, help='Name is required')
post_args.add_argument('created_at', type=str,
                       required=True, help='Created_at is required')
post_args.add_argument('updated_at', type=str,
                       required=True, help='Updated_at is required')


class CategoryById(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            abort(404, message=f"category with id {id} doesn't exist")
        result = category_schema_single.dump(category)
        return jsonify(result)

class CategoryById(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            abort(404, message=f"Category with ID {id} doesn't exist")
        result = category_schema_single.dump(category)
        return jsonify(result)
    

    # *Update: PUT/PATCH*
    def patch(self, id):                                 
        category = Category.query.get(id)
        if not category:
            abort(404, message="Not found")
        
        data = patch_args.parse_args()
        for key, value in data.items():   
            if value is not None:
                setattr(category, key, value)
        
        db.session.commit()
        result = category_schema_single.dump(category)
        return jsonify(result)


    def delete(self, id):
        category = Category.query.get(id)
        if not category:
            abort(404)

        db.session.delete(category)
        db.session.commit()
        return f'category with {id=} has been deleted.', 204


api.add_resource(Category, '/category')
api.add_resource(CategoryById, '/category/<string:id>')

# Create: POST
# Read: GET
# Update: PUT/PATCH
# Delete: DELETE