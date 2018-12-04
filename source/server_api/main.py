from flask import Flask 
from flask_restful import Resource, Api, reqparse


from predict.predictSeccionTema import PredictSeccionTema
from predict.template_classes import normalize_text

#import  predict.template_classes 
# from predict.template_classes import normalize_text
# import predict.predictSeccionTema

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

#init DNN
clasifier = PredictSeccionTema(root_path = "/opt/NLP_pedro/",
            features_path = 'data/features/',
            feature_file = "calcFeat_tfid_hash28_n10000_svd1000.p",
            path_model_seccion = 'models/test/',
            path_model_tema = 'models/seccion/')


class root(Resource):
    def get(self):
        return {'quote': ['api clasificadora de noticias'] }
    
        

class clasifiNotic(Resource):   
    def post(self):
        """ recive tipo x-www-form-urlencoded """
        parser.add_argument('cuerpo', type=str)
        args = parser.parse_args() # json de request
        cuerpo = args['cuerpo']
        seccion, tema = clasifier.predict(cuerpo)
        return {
            'status' : True,
            'tema' : tema,
            'seccion' : seccion            
        }        
#paths
api.add_resource(root, '/') 
api.add_resource(clasifiNotic, '/api/altavoz/beta/clasificador') 



if __name__ == '__main__':
    api.app.run(debug=True, host= '0.0.0.0', port=5005)