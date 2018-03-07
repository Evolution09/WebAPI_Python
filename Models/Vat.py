from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


class Vat(db.Model):
    __tablename__ = 'vat_dict'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), unique=True)
    Code = db.Column(db.String(30), unique=True)
    Value = db.Column(db.Float(10, 0), unique=True)

    def __init__(self, name, code, value):
        self.Name = name
        self.Code = code
        self.Value = value

    def serialize(self):
        return \
            {
                'Name': self.Name,
                'Code': self.Code,
                'Value': self.Value
            }

    def __repr__(self):
        return '<VAT %r %r >' % (self.Code, self.Name)


