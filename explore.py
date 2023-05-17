import pandas as pd
import acquire
from prepare import basic_prepare

import re
import unicodedata
import pandas as pd
import nltk

import matplotlib.pyplot as plt
from wordcloud import WordCloud


df = pd.read_csv('github_data.csv')
df = basic_prepare(df)

def clean(text):
    'A simple function to cleanup text data'
    wnl = nltk.stem.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english') + ['java', 'python', 'javascript', 'c']
    text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwords]

# getting list of words for each 
javascript_words = clean(' '.join(df[df.language == 'JavaScript'].spacy))
java_words = clean(' '.join(df[df.language == 'Java'].spacy))
c_words = clean(' '.join(df[df.language == 'C'].spacy))
python_words = clean(' '.join(df[df.language == 'Python'].spacy))
all_words = clean(' '.join(df.spacy))

# getting words frequencies
javascript_freq = pd.Series(javascript_words).value_counts()
java_freq = pd.Series(java_words).value_counts()
c_freq = pd.Series(c_words).value_counts()
python_freq = pd.Series(python_words).value_counts()
all_freq = pd.Series(all_words).value_counts()


# THe is an collection of alll the words anc things, It seems that the cleaning done needs to be improved for the results of this to come back with something useful. I seem to have made mostakes in the cleaning process
word_counts = (pd.concat([all_freq, c_freq, java_freq, javascript_freq, python_freq], axis=1, sort=True)
                .set_axis(['all', 'c', 'java', 'javascript', 'python'], axis=1, inplace=False)
                .fillna(0)
                .apply(lambda s: s.astype(int)))

# figure out the percentage of word counts for each
def get_perc_word_count():
    '''
    
    '''

    (word_counts
     .assign(p_python=word_counts.python / word_counts['all'],
             p_java=word_counts.java/ word_counts['all'],
            p_javascript=word_counts.javascript/ word_counts['all'],
            p_c=word_counts.c / word_counts['all'])
     .sort_values(by='all')
     [['p_python', 'p_java', 'p_javascript', 'p_c']]
     .tail(20)
     .plot.barh(stacked=True))

    plt.title('Proportion of Python, Java, JavaScript, & C for the 20 most common words')
    
    return

def get_common_words():
    
    # figure out the percentage of spam vs ham
    word_counts['all'].sort_values(ascending=False).head(20).plot.barh()

    plt.title('Counts of the 20 Most Common Words')
    plt.show()
    return




############ MODELING #########################
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

# basic x and y
X = df.spacy
y = df.language

X2, X_test, y2, y_test = train_test_split(X, y, stratify=y, test_size=.1)

X_train, X_validate, y_train, y_validate = train_test_split(X2, y2, stratify=y2, test_size=.2)


tfidf = TfidfVectorizer()
X_train = tfidf.fit_transform(X_train)
X_validate = tfidf.transform(X_validate)

train = pd.DataFrame(dict(actual=y_train))
validate = pd.DataFrame(dict(actual=y_validate))

lm = LogisticRegression().fit(X_train, y_train)

train['predicted'] = lm.predict(X_train)
validate['predicted'] = lm.predict(X_validate)



def results1():
    ''''''
    print('Accuracy: {:.2%}'.format(accuracy_score(train.actual, train.predicted)))
    print('---')
    print('Confusion Matrix')
    print(pd.crosstab(train.predicted, train.actual))
    print('---')
    print(classification_report(train.actual, train.predicted))
    return

def results2():
    '''
    '''
    print('Accuracy: {:.2%}'.format(accuracy_score(validate.actual, validate.predicted)))
    print('---')
    print('Confusion Matrix')
    print(pd.crosstab(validate.predicted, validate.actual))
    print('---')
    print(classification_report(validate.actual, validate.predicted))
    return