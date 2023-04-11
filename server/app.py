#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'

class Index(Resource):
    def get(self):
        return make_response('<h1>Code challenge</h1>', 200)
    
api.add_resource(Index, '/')

class ResearchController(Resource):
    def get(self):
        return make_response([research.to_dict(only = ('id', 'topic', 'year', 'page_count')) for research in Research.query.all()], 200)
        # research_list = []
        # for research in query:
        #     new_research = {
        #         "id": research.id,
        #         "topic": research.topic,
        #         "year": research.year,
        #         "page_count": research.page_count
        #     }
        #     research_list.append(new_research)
        # return make_response(research_list, 200)

api.add_resource(ResearchController, '/research')

class ResearchById(Resource):
    def get(self, id):
        return make_response(Research.query.filter(Research.id == id).first().to_dict(), 200) if Research.query.filter(Research.id == id).first() else make_response({"error": "Research paper not found"}, 404)
    def delete(self, id):
        if Research.query.filter(Research.id == id).first():
            db.session.delete(Research.query.filter(Research.id == id).first())
            db.session.commit()
        else:
            return make_response({"error": "Research paper not found"}, 404)

api.add_resource(ResearchById, '/research/<int:id>')

class AuthorsController(Resource):
    def get(self):
        return make_response([author.to_dict(only = ('id', 'field_of_study', 'name')) for author in Author.query.all()], 200)
    
api.add_resource(AuthorsController, '/authors')

class ResearchAuthorsController(Resource):
    def post(self):
        try:
            new_ra = ResearchAuthors(
                author_id = request.get_json()['author_id'],
                research_id = request.get_json()['research_id']
            )
            db.session.add(new_ra)
            db.session.commit()

            return make_response(new_ra.to_dict()['author'], 201)
        except Exception:
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(ResearchAuthorsController, '/research_author')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
