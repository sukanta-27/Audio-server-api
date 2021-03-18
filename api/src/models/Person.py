from api import db

class Person(db.Model):
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
