from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

fields = ['AI',
                  'Robotics',
                  'Machine Learning',
                  'Vision',
                  'Cybersecurity'
                  ]

class Research(db.Model, SerializerMixin):
    __tablename__ = 'researches'

    serialize_rules = ('-research_authors.research',)

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', backref='research', cascade='all, delete, delete-orphan')

    @validates('year')
    def validate_number(self, key, number):
        if number < 1000 or number > 9999:
            raise ValueError("Year must be a 4 digit number")
        return number
    
class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research_authors.author',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_authors = db.relationship('ResearchAuthors', backref='author')

    @validates('field_of_study')
    def validate_month(self, key, field):
        if field not in fields:
            raise ValueError("Field of Study must be one of the following: [AI, Robotics, Machine Learning, Vision, Cybersecurity]")
        return field

class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-research.research_authors', '-author.research_authors',)

    id = db.Column(db.Integer, primary_key=True)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())