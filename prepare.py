## install these packages before running
# !pip install -U spacy
# !python -m spacy download en_core_web_sm

import pandas as pd
import re
import unicodedata
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import spacy


def basic_clean_keep_code(string):
    '''
    Takes in a string, makes all characters lowercase, normalizes all characters, and removes unnnecessary special characters
    import re
    import unicodedata
    '''
    # Remove line breaks
    string = re.sub(r'\n', ' ', string)
    
    # Remove the urls
    string = re.sub(r'https?://[^\s]+', '', string)
    
    # lowercase all words
    lowered = string.lower()

    # normalize unicode characters using lowered
    normalized = unicodedata.normalize('NFKD', lowered).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # replacing unnecessary characters from normalized
    cleaned = re.sub(r"[^a-z0-9'\s]", '', normalized)
    
    return cleaned

def tokenize(string):
    '''
    Takes in a string and tokenizes the string
    Modules:
        from nltk.tokenize.toktok import ToktokTokenizer
    '''
    # initialize tokenizers
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # tokenize string and store in tokenized
    tokenized = tokenizer.tokenize(string, return_str=True)
    
    return tokenized


def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    takes in a string and removes stopwords using the stopwords
    Modules:
         from nltk.corpus import stopwords
    '''
    # establish stop word list
    stop_word_list = stopwords.words('english')
    
    # if there are any words in the kwarg
    if bool(extra_words) == True:

        # add them to the stop_word_list
        stop_word_list = stop_word_list + extra_words

    # if there are any words in the kwarg
    if bool(exclude_words) == True:

        # remove them from the stop word list
        stop_word_list = [word for word in stop_word_list if word not in exclude_words]
        
    # getting a list of words from string argument that are not in the list of stop words (removing the stopwords)
    filtered = [word for word in string.split() if word not in stop_word_list]
    
    # rejoin all the words in the lsit with a space to reform string
    string_without_stopwords = ' '.join(filtered)
    
    # exit and return the string
    return string_without_stopwords

def cleaned_with_code_included(x):
    '''
    Takes in a string literal and performs cleaning, tokenizing, and removes the stop words
    
    '''
    # runs a basic clean
    x = basic_clean_keep_code(x)
    
    # tokenizes the words
    x = tokenize(x)
    
    # removes the stop words
    x = remove_stopwords(x)
    
    # returns string with all cleaning steps performed
    return x

def lemmatize(string):
    '''
    Takes in a string and returns it with all words in lemmatized form
    Modules:
        import nltk
    '''
    # initializing lematizing object
    wnl = nltk.stem.WordNetLemmatizer()

    # getting a list of root words from each word in the split string
    lemmas = [wnl.lemmatize(word) for word in string.split()]

    # rejoining the list of root words to form a lemmatized corpus
    lemmatized = ' '.join(lemmas)
    
    # exit and return lemmatized info
    return lemmatized

def spacy_string(string):
    '''
    Takes in a string and returns it with all words in spacy-lemmatization form form
    Modules:
        import spacy
    '''
    # initializing lematizing object
    nlp = spacy.load('en_core_web_sm')
    
    # getting lemmatized words
    string_stemmed = [word.lemma_ for word in nlp(string)]
    
    # rejoining words
    string_stemmed = ' '.join(string_stemmed)
    
    # exit and return lemmatized info
    return string_stemmed

def basic_prepare(df):
    '''
    Takes in a df and adds columns with cleaned code
    '''
    
    # initial cleaning completed
    df['basic_clean_with_code'] = df['readme_contents'].apply(lambda x: cleaned_with_code_included(x))
    
    # getting spacy stemming
    df['spacy'] = df['basic_clean_with_code'].apply(lambda x: spacy_string(x))
    
    # getting lemmatized text
    df['lem'] = df['basic_clean_with_code'].apply(lambda x: lemmatize(x))
    
    return df
