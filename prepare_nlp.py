# imports 
import pandas
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


def basic_clean(string):
    '''
    Takes in a string, makes all characters lowercase, normalizes all characters, and removes unnnecessary special characters
    import re
    import unicodedata
    '''
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

def stem(string):
    '''
    Takes in a string and stems all words in tthe string, returrning a stemmed version of it
    Modules:
        import nltk
    '''
    # initialize stem object
    ps = nltk.porter.PorterStemmer()

    # get a list of stems for each word in the string
    stems = [ps.stem(word) for word in string.split()]

    # joining the words back together, using a space to separate each
    stemmed = ' '.join(stems)

    # getting the stemmedstring back
    return stemmed

def lemmatize(string):
    '''
    Takes in a string and returns it with all words in lemmatized form
    Modules:
        import nltk
    '''
    # initializing lematizing object
    wnl = nltk.stem.WordNetLemmatizer()

    # getting a list of root words from each word in the split string
    lemmas = [wnl.lemmatize(word) for word in tokenized.split()]

    # rejoining the list of root words to form a lemmatized corpus
    lemmatized = ' '.join(lemmas)
    
    # exit and return lemmatized info
    return lemmatized

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

def prepare_df(data, col: str, transpose = False):
    '''
    Takes in a list or a dictionary of text data, turns it into a dataframe, adds a cleaned data col, stemmed col, and lemmatized col
    Modules:
        import pandas as pd
    '''
    # if kwarg is true, 
    if transpose == True:
        
        # transpose the df (dict)
        df = pd.DataFrame(data).T
    
    # by default
    else:
        
        # create regular df with the data (list)
        df = pd.DataFrame(data)
    
    # apply the basic clean function to the text col and add to the df as a new col
    df['clean'] = df[col].apply(basic_clean)
    
    # apply stem function to cleaned col and add to the df as a new col
    df['stemmed'] = df.clean.apply(stem)
    
    # apply lemmatize funtion to cleaned col and add to the df as a new col
    df['lemmatized'] = df.clean.apply(lemmatize)
    
    # returned prepped df
    return df
