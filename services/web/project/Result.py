from flask_restful import Resource
from flask import request
from .AddressModel import AddressModel


class Result(Resource):
    def get(self):
        response = {'points': [], 'links': [], 'request_id':''}
        address = AddressModel()
        request_id = request.args.get('request_id')
        response['request_id'] = request_id
        points = address.get_all_points(request_id)
        links = address.get_all_result(request_id)
        for row in points:
            response['points'].append({
                'point': row['point'],
                'address': row['address']})

        for row in links:
            response['links'].append({
                'name': row['links'],
                'distance': row['distance']})

        return response
