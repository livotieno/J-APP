from flask import Blueprint, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_marshmallow import Marshmallow

from models import Entry, db

from serializers import EntrySchema

entry_bp = Blueprint('entry_bp', __name__)
ma = Marshmallow(entry_bp)
api = Api(entry_bp)

post_args = reqparse.RequestParser()
post_args.add_argument('id', type=str,
                       help='id is required')
post_args.add_argument('user_id', type=str,
                       required=True, help='id is required')
post_args.add_argument('title', type=str,
                       required=True, help='title is required')
post_args.add_argument('content', type=str,
                       required=True, help='id is required')
post_args.add_argument('category', type=str,
                       required=True, help='category is required')
post_args.add_argument('created_at', type=str,
                       required=True, help='Created_at is required')
post_args.add_argument('updated_at', type=str,
                       required=True, help='Updated_at is required')

class EntryById(Resource):
    def get(self, id):
        entry = Entry.query.get(id)
        if not entry:
            abort(404, message=f"category with id {id} doesn't exist")
        result = entry_schema_single.dump(category)
        return jsonify(result)

class EntryById(Resource):
    def get(self, id):
        entry = entry.query.get(id)
        if not entry:
            abort(404, message=f"Category with ID {id} doesn't exist")
        result = entry_schema_single.dump(entry)
        return jsonify(result)
    
    def patch(self, id):
        entry = Entry.query.get(id)
        if not entry:
            abort(404, message="Not found")
        
        data = patch_args.parse_args()
        for key, value in data.items():   
            if value is not None:
                setattr(entry, key, value)
        
        db.session.commit()
        result = entry_schema_single.dump(entry)
        return jsonify(result)


    def delete(self, id):
        entry = Entry.query.get(id)
        if not entry:
            abort(404)

        db.session.delete(entry)
        db.session.commit()
        return f'entry with {id=} has been deleted.', 204


api.add_resource(Entry, '/entry')
api.add_resource(EntryById, '/Entry/<string:id>')
