from flask import Flask,  request, make_response
from flask_restful import Resource, Api
from Redis import Redis
import json
from Query import Query
from logger import logging

app = Flask(__name__)
api = Api(app)


class PostQuery(Resource):
    def post(self):
        if request.is_json:
            try:
                args = request.args
                phone = args.get("phone")
                if phone == "" or phone is None:
                    raise Exception("Phone Number is required")
                name = args.get("name")
                if name == "" or name is None:
                    raise Exception("Name is required")
            except Exception as e:
                logging.error('Phone Number and Name is required')
                return {'status': "failed", 'error': 'Phone Number and Name is required'},
            else:
                redisObj = Redis()
                query = request.json["query"]
                queryObj = Query(name,query,phone)
                redisObj.add_query(queryObj)
                logging.info({'status': 'Success'})
                return make_response(json.dumps({'status': 'Success'}), 201)
        else:
            logging.error('Request must be JSON')
            return {'status': "failed", 'error': 'Request must be JSON'}, 400

@app.errorhandler(404)
def invalid_route(e):
    logging.error({'status': "failed", 'error': 'Invalid Route'})
    return {'status': "failed",'error': 'Invalid Route'}, 404

api.add_resource(PostQuery, '/query')

if __name__ == "__main__":
    app.run()
