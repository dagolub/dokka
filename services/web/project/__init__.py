from flask import Flask, request
from flask_restful import Api
from flask_restful import Resource
import uuid
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
api = Api(app)


class AddressDb(db.Model):
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    point = db.Column(db.String(1), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)


class Address(Resource):
    def get(self):
        return {'ppp': 234}

    def post(self):
        request_id = uuid.uuid4()

        self.save_addresses(request_id, pd.read_csv(request.files['file']))

        return {'request_id': request_id.__str__()}

    def save_addresses(self, request_id, data):
        i = 0
        for point in data['Point']:
            row = AddressDb(request_id=request_id,
                            point=point,
                            longitude=data['Longitude'][i],
                            latitude=data['Latitude'][i])
            db.session.add(row)
            db.session.commit()
            i += 1

api.add_resource(Address, '/api/address')
# api.add_resource(Result, '/api/result')

if __name__ == '__main__':
    app.run(debug=True)
