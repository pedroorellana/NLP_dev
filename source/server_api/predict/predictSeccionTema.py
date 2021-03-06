
# coding: utf-8

import pickle
import time

import  time, string, unicodedata
import tensorflow as tf
import numpy as np
from tensorflow.contrib.learn import DNNClassifier
from predict.normalize_text import normalize_text




class PredictSeccionTema:
    """ clase para predecir seccion y tema """
    def __init__(self, root_path , feature_file , features_path , path_model_seccion , path_model_tema ):
        self.root_path = root_path
        self.feature_file = feature_file
        self.features_path = self.root_path + features_path
        self.features_path_ = self.features_path +  self.feature_file
        self.path_model_seccion = self.root_path + path_model_seccion
        self.path_model_tema = self.root_path + path_model_tema

        # ### carga info modelos y clase extractor features TFIDF+SVF
        self.labels_tema_all = pickle.load( open( self.path_model_tema+ "info_model.p", "rb" ) )[1]
        self.labels = pickle.load( open( self.path_model_seccion + "info_model.p", "rb" ) )[1]
        import runpy
        runpy._run_module_as_main("normalize_text")


        wb,svdT,non_zero_index_feat = pickle.load( open( self.features_path_, "rb" ) )

        # ### carga modelo DNN seccion y extrac feat tfidf
        self.sec1 = DnnEval(self.labels , self.path_model_seccion ,1000)
        self.tfidf_svd_model = TfidfSvd(wb,svdT,non_zero_index_feat)
    
    def predict(self, text_input):
        # ### evalua una entrada de test ( calc feat e inferencia)
        feat_vec = self.tfidf_svd_model.calcFeat(text_input)
        top3ClasesS, top3ProbS, labelsS, pred_probS = self.sec1.calcPred( vec_input = feat_vec)
        
        # ### clasificador de tema carga modelo a partir de seccion predicha
        self.path_model_tema_ = self.path_model_tema + "/" + top3ClasesS[0]
        self.labels_tema = self.labels_tema_all[top3ClasesS[0]]
        tema1 = DnnEval(self.labels_tema, self.path_model_tema_,1000)

        top3ClasesT, top3ProbT, labelsT, pred_probT = tema1.calcPred( vec_input = feat_vec)
        print( "seccion : " +top3ClasesS[0]+ "\ntema: "+top3ClasesT[0] + "\n")
        return(top3ClasesS, top3ProbS, labelsS, pred_probS, top3ClasesT, top3ProbT, labelsT, pred_probT)
        #return 0


class TfidfSvd:
    """ extractor features tfidf + svd"""
    def __init__(self, wordbach_trained , svd_trained,non_zero_index_feat):
        self.wordbach = wordbach_trained
        self.svdT = svd_trained
        self.non_zero_index_feat = non_zero_index_feat
        self.normalize_text = wordbach_trained.normalize_text


    
    def calcFeat(self,text):
        """calcula features tfidf + svd """      
        self.tfidf = self.wordbach.transform([self.normalize_text(text)])
        self.tfidf = self.tfidf[:, self.non_zero_index_feat]
        TfidfSvd = self.svdT.transform(self.tfidf)
        return(TfidfSvd)

class DnnEval:
    """ DNN eval para prediccion"""
    def __init__(self, labels, path_model,dim_vec_input):
        self.path_model = path_model
        self.labels = labels        
        self.nClasses = len(self.labels)
        self.feature_columns = [tf.contrib.layers.real_valued_column('x', dimension = dim_vec_input)]
        self.classifier = DNNClassifier(                                
                                   n_classes=len(labels), label_keys=self.labels, 
                                   feature_columns=self.feature_columns,
                                   hidden_units=[2000], 
                                   model_dir = self.path_model                         
                                  )
    def input_fn_evaluate(self):
        input = {'x': tf.constant(self.vec_input )}    
        return input    

    def calcPred(self,vec_input):
        """ calcula prediccion """
        self.vec_input = vec_input
        pred_prob = self.classifier.predict_proba(input_fn=self.input_fn_evaluate)
        pred_prob = [x for x in list(pred_prob)]
        pred_prob = pred_prob[0]

        index_sorted_prob = np.argsort(pred_prob)
        top3Clases= [ self.labels[index_sorted_prob[-1]] ,
                      self.labels[index_sorted_prob[-2]] ,
                      self.labels[index_sorted_prob[-3]] , 
                    ]

        top3Prob= [ pred_prob[index_sorted_prob[-1]] ,
                    pred_prob[index_sorted_prob[-2]] ,
                    pred_prob[index_sorted_prob[-3]] ,
                  ]

        return ( top3Clases, top3Prob, self.labels, pred_prob ) 



def main():
    # test tex
    clasifier = PredictSeccionTema(root_path = "../../",
                    feature_file = "calcFeat_tfid_hash28_n10000_svd1000.p",
                    features_path = 'data/features/',
                    path_model_seccion = 'models/test/',
                    path_model_tema = 'models/seccion/')

    test_text = 'Un total de 916 personas murieron en acciones que involucraron a la policía y otras 2.989 fallecieron en homicidios dolosos, durante los ochos meses de intervención de la seguridad pública en Río de Janeiro, la ciudad más emblemática de Brasil, según informe divulgado este lunes por una ONG.Las muertes de miembros de la Policía y el Ejército durante el período en que ha sido implementada la intervención, también fueron retomadas en el informe, según el cual 74 agentes han fallecido entre febrero y octubre de 2018."Las políticas de guerra contra las drogas y los enfrentamientos como método de seguridad pública son responsables por los inaceptables números de Río de janeiro: además de las muertes de civiles y militares, casi mil muertes de civiles por acción policial", aseguró el informe de la ONG.Los datos se recogen en un informe divulgado este martes por el Observatorio de la Intervención del Centro de Estudios de Seguridad y Ciudadanía de la Universidad brasileña Cándido Mendes, a través de las redes sociales.'
    clasifier.predict(test_text)
    test_text = 'El Banco Falabella se convertirá en el mayor emisor de tarjetas de crédito del país, después de que la Superintendencia de Bancos e Instituciones Financieras (SBIF) aprobara la integración de CMR Falabella a la compañía. La figura bajo la cual CMR se integra a Banco Falabella es la de Sociedad de Apoyo al Giro (SAG). Con esto, Banco Falabella será el mayor emisor de tarjetas de crédito del país, con una cantidad superior a los 3 millones de ellas activas, según Diario Financiero.'
    clasifier.predict(test_text)

if __name__ == '__main__':
    main()