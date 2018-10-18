from flask import Flask 
from flask_restful import Resource, Api, reqparse



app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class root(Resource):
    def get(self):
        return {'quote': ['api clasificadora de noticias'] }
    
    def post(self):
        """ recive tipo x-www-form-urlencoded """
        args = parser.parse_args() # json de request
        parser.add_argument('cuerpo', type=str)

        return {
            'status': True,
            'cuerpo': '{} added. Good'.format(args['cuerpo'])
        }


api.add_resource(root, '/')

if __name__ == '__main__':
    app.run(debug=True)