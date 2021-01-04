from flask_restful import Resource
from flask import request, json
from .AddressModel import AddressModel
from redis import Redis


class Result(Resource):
    def __init__(self):
        self.cache = Redis('redis')
    def get(self):
        request_id = request.args.get('request_id')
        data = self.cache.get(name=request_id)
        if data:
            response = json.loads(data)
            return response

        response = {'points': [], 'links': [], 'request_id': ''}
        address = AddressModel()
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

        self.cache.set(name=request_id, value=json.dumps(response))
        return response
