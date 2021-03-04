import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
import string
import gensim
import re
import pandas as pd
from gensim.models.ldamodel import LdaModel 
#from googletrans import Translator
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer, SnowballStemmer
nltk.download('wordnet')
nltk.download('punkt')


# Remove emojies  
def Remove_Emojy(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# Clean text
def remove_nan(text):
    if text == 'No caption':
        return ''
    return text

#translator = Translator()

def pre_process(text):
    
    text = Remove_Emojy(text)
    text = remove_nan(text)
    # Translate caption to english
    #text = translator.translate(text).text
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words and replace non-ascii characters
    stop_words = set(stopwords.words('english'))
    words = [unidecode(w) for w in words if not w in stop_words]
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens.
    words = [word for word in words if word.isalpha()]
    stemmer = SnowballStemmer('english')
    words = [stemmer.stem(WordNetLemmatizer().lemmatize(word)) for word in words]
    return " ".join(words)


# Number of hashtags and References
def hashtags_num(text):
    return len(re.findall(r"#(\w+)", text))

def ref_num(text):
    return len(re.findall(r"@(\w+)", text))

# Sentimental Analysis:
def polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity 

def sentiment(polarity):
    if polarity > 0:
        val = "positive"
    elif polarity == 0:
        val = "neutral"
    else:
        val = "negative"
    return val

#Topic modeling
def LDAmodel(X,passes=2,num_topics=10,workers = 2,re_train=False):
    tokens = []
    for c in X:
        tokens.append(c.split())
    dictionary = gensim.corpora.Dictionary(tokens)
    bow_corpus = [dictionary.doc2bow(caption) for caption in tokens]
    if (re_train == True):
        ldamodel =  gensim.models.LdaMulticore(bow_corpus,
                                           num_topics=num_topics,
                                           id2word = dictionary,                                    
                                           passes = passes,
                                           workers = workers)
        ldamodel.save("data/3_topic_modeling_weights//ldamodel_weights")
    else:
        ldamodel = LdaModel.load("data/3_topic_modeling_weights//ldamodel_weights")
        
    sent_topics_df = pd.DataFrame()
    for i, row in enumerate(ldamodel[bow_corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                sent_topics_df = sent_topics_df.append(pd.Series([str(int(topic_num)),
                                                                  round(prop_topic,4)]),
                                                       ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['dominant_topic', 'perc_contribution']

    return sent_topics_df


