import numpy as np
import pandas as pd

import re
from bs4 import BeautifulSoup
import nltk
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.tokenize import ToktokTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag.util import untag



n_most_frequent_tag = pd.read_csv('data/n_most_frequent_tag.csv', sep=',', header = None, index_col = 0, squeeze = True)

def clean_title_question(text1, text2):
    text1 = clean_text(text1) 
    text2 = clean_text(text2)
    text = text1 + ' ' + text2
    text = pd.Series([text])
    return text

def clean_text(text):
    text = remove_html(text)
    text = remove_elision(text)
    text = lemitizeWords(text)
    text = clean_punct(text)
    text = stopWordsRemove(text)
    RemoveWords_by_tag(text)
    return text

def remove_html(text):
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text

def remove_elision(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub(r"\'\n", " ", text)
    text = re.sub(r"\'\xa0", " ", text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

lemma=WordNetLemmatizer()

def lemitizeWords(text):
    words=token.tokenize(text)
    listLemma=[]
    for w in words:
        x=lemma.lemmatize(w, pos="v")
        listLemma.append(x)
    return ' '.join(map(str, listLemma))


token=ToktokTokenizer()

charac = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789'

def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']

def clean_punct(text): 
    words=token.tokenize(text)
    punctuation_filtered = []
    regex = re.compile('[%s]' % re.escape(charac)) # Échappe toutes les punctuations
    remove_punctuation = str.maketrans(' ', ' ', charac)
    for w in words:
        if w in n_most_frequent_tag:
            punctuation_filtered.append(w)
        else:
            punctuation_filtered.append(regex.sub('', w))
  
    filtered_list = strip_list_noempty(punctuation_filtered)
        
    return ' '.join(map(str, filtered_list))


def stopWordsRemove(text):
    
    stop_words = set(stopwords.words("english"))
    
    words=token.tokenize(text)
    
    filtered = [w for w in words if not w in stop_words]
    
    return ' '.join(map(str, filtered))


def RemoveWords_by_tag(text):
    remove_tag_list = ['JJ','JJR', 'JJS', 'RBR', 'RBS']
    token=ToktokTokenizer()
    words=token.tokenize(text)
    words_tagged = nltk.pos_tag(words)
    filtered = untag([w for w in words_tagged if not w[1] in remove_tag_list]) # Filtre les mots qui n'appartiennt pas à la catégorie à supprimer
    
    return ' '.join(map(str, filtered))