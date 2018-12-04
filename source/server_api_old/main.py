from flask import Flask 
from flask_restful import Resource, Api, reqparse



app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class root(Resource):
    def get(self):
        return {'quote': ['api clasificadora de noticias'] }
    

class clasificationText(Resource):
    
    def post(self):
        """ recive tipo x-www-form-urlencoded """
        parser.add_argument('cuerpo', type=str)
        args = parser.parse_args() # json de request
        cuerpo = args['cuerpo']

        return {
            'status': True,
            'cuerpo': '{} added. Good'.format(cuerpo)
        }

api.add_resource(root, '/')
api.add_resource(clasificationText, '/api/altavoz/beta/clasificar')


if __name__ == '__main__':
    print("s")
    #app.run(debug=True)
    api.app.run(debug=True, host= '0.0.0.0', port=5005)