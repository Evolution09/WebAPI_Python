from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('Country', 'City', 'Street', 'Street_details', 'Apartament_no')
