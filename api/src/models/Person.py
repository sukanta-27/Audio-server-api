from api import db

class Person(db.Model):
    """
    Person class is a SQLAlchemy model that is used as a base class 
    for all the supported roles: Host, Participant, Author, Narrator

    The relationship between the subclasses follow the "Joined Table Inheritance" (https://docs.sqlalchemy.org/en/13/orm/inheritance.html)

    fields:
        id: Integer,
        name: String [max length = 100],
    """

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'person'
    }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"name: {self.name}, type: {self.type}"
