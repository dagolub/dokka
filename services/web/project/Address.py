from flask_restful import Resource
import csv
from flask import request
import uuid
import os
from .AddressModel import AddressModel
from .get_address import get_address
from redis import Redis
from rq import Queue
q = Queue(connection=Redis('redis'))


class Address(Resource):
    def get(self):
        response = []
        address = AddressModel()
        result = address.get_all_points()
        for row in result:
            response.append({
                'point': row['point'],
                'lat': row['latitude'],
                'lon': row['longitude'],
                'address': row['address']})
        return response

    def post(self):
        request_id = uuid.uuid4()
        file = request.files['file']
        file_path = os.path.join("uploads", request_id.__str__() + ".csv")
        file.save(file_path)
        with open(file_path, 'r') as file:
            input = csv.reader(file)
            next(input)
            for row in input:
                point, latitude, longitude = row
                row = AddressModel(request_id=request_id, point=point, longitude=longitude, latitude=latitude)
                row.save()
        q.enqueue(get_address, request_id)

        return {'request_id': request_id.__str__()}
