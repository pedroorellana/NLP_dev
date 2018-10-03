import tensorflow as tf
import _pickle as pickle
import pandas as pd
import numpy as np
import os, time
import unidecode

import nltk
from nltk.corpus import stopwords

from tensorflow.contrib.learn import LinearClassifier
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


def remove_accents(a):
    return unidecode.unidecode(a)


def normalize_text(text):
    return u" ".join([x for x in [y for y in text.lower().strip().split(" ")] 
                      if len(x) > 1 and x not in spanish_stopwords])

def get_test_inputs():
    X_ = X_transformed
    x= X_.todense()
    dataset = tf.estimator.inputs.numpy_input_fn({'': x}, shuffle=False, num_epochs=1)
    return dataset
def tokenizer(text):
    words = nltk.word_tokenize(text)
    return words

with open('tfidf.pk', 'rb') as file:
    tfidf = pickle.load(file)
print('Introduzca el cuerpo de la noticia:')
text = input()

t0 = time.time()
X_transformed = tfidf.transform([text])
print(time.time() - t0)


nClasses = 9
labels = ['Deportes', 'Pais', 'Entretencion', 'Mundo', 'Economia', 'Cultura', 'Sociedad', 'Tecnologia', 'Corporativo']
labels_tilde = ['Deportes', 'País', 'Entretención', 'Mundo', 'Economía', 'Cultura', 'Sociedad', 'Tecnología', 'Corporativo']

feature_columns = [tf.contrib.layers.real_valued_column("", dimension=1000)]

t0 = time.time()
classifier = LinearClassifier(n_classes=nClasses, label_keys=labels, feature_columns=feature_columns, model_dir='./model/seccion')
# print(time.time() - t0)

t0 = time.time()
pred_test = classifier.predict_classes(input_fn=get_test_inputs())
# print(time.time() - t0)


# print(list(classifier.predict_proba(input_fn=get_test_inputs())))


predicted_section_str = list(pred_test)[0].decode('UTF-8')
print('Seccion: {}'.format(predicted_section_str))

predicted_section_str_normalized = remove_accents(predicted_section_str.lower())
model_tema_path = './model-parallel/{}'.format(predicted_section_str_normalized)

# print("spanish_stopwords...", end='')
spanish_stopwords = stopwords.words('spanish')
# print("done.")

labels_tema = None
with open('labels.pk', 'rb') as file:
    labels_tema = pickle.load(file)

wb = None
with open('tfidf-tema-parallel.pk', 'rb') as file:
    wb = pickle.load(file)
    
index = labels.index(predicted_section_str)
section = labels_tilde[index]
features_tema = wb[section].transform([text])

feature_columns_tema = {}
classifier_tema = {}
nClasses_tema = {'Deportes': 38, 'Entretención': 15, 'País': 61, 'Mundo': 40, 'Economía': 18, 'Cultura': 18, 'Sociedad': 23, 'Tecnología': 6, 'Corporativo': 2}

if predicted_section_str == 'Corporativo':
    feature_columns_tema = [tf.contrib.layers.real_valued_column("", dimension=1000)]
    classifier_tema      = LinearClassifier(n_classes=nClasses_tema[section], feature_columns=feature_columns, model_dir=model_tema_path)
else: 
    feature_columns_tema[section] = [tf.contrib.layers.real_valued_column("", dimension=1000)]
    classifier_tema          = LinearClassifier(n_classes=nClasses_tema[section], label_keys=labels_tema[section], feature_columns=feature_columns, model_dir=model_tema_path)
    
pred_test_tema = classifier_tema.predict_classes(input_fn=get_test_inputs())

predicted_tema =  list(pred_test_tema)[0].decode('UTF-8')
print('Tema: {}'.format(predicted_tema))

