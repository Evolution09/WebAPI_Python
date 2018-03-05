from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('Name', 'Code', 'Description')
