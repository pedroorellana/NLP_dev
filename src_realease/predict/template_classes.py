
import  time, string, unicodedata
import tensorflow as tf
import numpy as np
from tensorflow.contrib.learn import DNNClassifier
# Representation
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
#Carga stop word
#nltk.download('stopwords')
spanish_stopwords = nltk.corpus.stopwords.words('spanish')

test_text = 'Un total de 916 personas murieron en acciones que involucraron a la policía y otras 2.989 fallecieron en homicidios dolosos, durante los ochos meses de intervención de la seguridad pública en Río de Janeiro, la ciudad más emblemática de Brasil, según informe divulgado este lunes por una ONG.Las muertes de miembros de la Policía y el Ejército durante el período en que ha sido implementada la intervención, también fueron retomadas en el informe, según el cual 74 agentes han fallecido entre febrero y octubre de 2018."Las políticas de guerra contra las drogas y los enfrentamientos como método de seguridad pública son responsables por los inaceptables números de Río de janeiro: además de las muertes de civiles y militares, casi mil muertes de civiles por acción policial", aseguró el informe de la ONG.Los datos se recogen en un informe divulgado este martes por el Observatorio de la Intervención del Centro de Estudios de Seguridad y Ciudadanía de la Universidad brasileña Cándido Mendes, a través de las redes sociales.'

def normalize_text(text):
    """ Funcion de normalizacion de texto, acentos, tokenizacion y stemming"""    
    # split into words
    tokens = nltk.tokenize.word_tokenize(text,language='spanish', preserve_line=False)
    # convert to lower case
    tokens = [w.lower() for w in tokens]     
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]    
    # remove remaining tokens that are n<<<<<<<<<<<<<<<<<<<<<
    words = [word for word in stripped if word.isalpha()]    
    # stop word and remove accent
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    stop_words = set(spanish_stopwords)
    words = [strip_accents(w) for w in words if not w in stop_words]    
    stemmer = SnowballStemmer("spanish")
    out = ""
    for word in words:
        out += stemmer.stem(word)+" "    
    return out

class TfidfSvd:
    """ extractor features tfidf + svd"""
    def __init__(self, wordbach_trained , svd_trained,non_zero_index_feat,normalize_text):
        self.wordbach = wordbach_trained
        self.svdT = svd_trained
        self.non_zero_index_feat = non_zero_index_feat
        self.normalize_text = normalize_text
    
    def calc(self,text):
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

    def calc(self,vec_input):
        """ calcula prediccion """
        self.vec_input = vec_input
        pred_prob = self.classifier.predict_proba(input_fn=self.input_fn_evaluate)
        pred_prob = [x for x in list(pred_prob)]
        y_test_hat = self.labels[np.argmax(pred_prob)]
        return (y_test_hat , pred_prob[0])