from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


class ProducentSchema(ma.Schema):
    class Meta:
        fields = ('Name', 'Code', 'Telephone', 'Email', 'AddressID')
