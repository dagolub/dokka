from flask_restful import Resource
from flask import request
from .AddressModel import AddressModel


class Result(Resource):
    def get(self):
        response = {'points': [], 'links': []}
        address = AddressModel()
        points = address.get_all_points()
        links = address.get_all_result()
        for row in points:
            response['points'].append({
                'point': row['point'],
                'address': row['address']})

        for row in links:
            response['links'].append({
                'name': row['links'],
                'distance': row['distance']})

        return response
