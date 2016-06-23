from flask.views import MethodView
from flask_restful import reqparse
from flask import jsonify

class Github(MethodView):

    def post(self):
        args = self.parse_args()
        if self.verify_signature():
            if (args.event == 'ping'):
                response = jsonify({'msg': 'ok'})
            elif (args.event == 'push'):
                response = jsonify({'msg': 'push'})
                # service the push

            else:
                response = jsonify({'msg': 'unsupported event type: '+args.event})
                response.status_code = 400
        else:
            response = jsonify({'msg': 'bad signature'})
            response.status_code = 401
        return response

    def parse_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            name='X-Hub-Signature',
            location='headers',
            dest='sig',
            required=True,
            # help='github hmac hash'
        )
        parser.add_argument(
            name='X-GitHub-Event',
            location='headers',
            dest='event',
            required=True,
            # help='event type (ping, push, pr, etc.)'
        )
        args = parser.parse_args()
        return args

    def verify_signature(self):
        pass