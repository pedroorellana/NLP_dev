
import  time, string, unicodedata
import tensorflow as tf
import numpy as np
from tensorflow.contrib.learn import DNNClassifier



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