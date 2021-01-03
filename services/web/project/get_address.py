import os
from .app import db
from sqlalchemy.dialects.postgresql import UUID
from opencage.geocoder import OpenCageGeocode
from .AddressModel import AddressModel

geocoder = OpenCageGeocode('76b31bcf7f124310a4e76700542e1583')


def get_address(uuid):
    result = db.engine.execute("SELECT * FROM \"Address\" where request_id = '" + uuid.__str__() + "'")
    for row in result:
        model = AddressModel.query.get(row['id'])
        result = geocoder.reverse_geocode(row['latitude'], row['longitude'], language='en')
        model.address = result[0]['formatted']
        model.save()

