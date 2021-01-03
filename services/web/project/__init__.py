from .Address import Address
from .Result import Result
from .app import app, api


api.add_resource(Address, '/api/address')
api.add_resource(Result, '/api/result')

if __name__ == '__main__':
    app.run(debug=True)
