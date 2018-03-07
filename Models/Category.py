from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'category_dict'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), unique=True)
    Code = db.Column(db.String(30), unique=True)
    Description = db.Column(db.String(300))

    def __init__(self, name, code, description):
        self.Name = name
        self.Code = code
        self.Description = description

    def serialize(self):
        return \
            {
                'Name': self.Name,
                'Code': self.Code,
                'Description': self.Description
            }

    def __repr__(self):
        return '<Category %r %r >' % (self.Code, self.Name)


