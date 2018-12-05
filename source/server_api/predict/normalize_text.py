
import  time, string, unicodedata
# Representation
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
#Carga stop word
#nltk.download('stopwords')
spanish_stopwords = nltk.corpus.stopwords.words('spanish')



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