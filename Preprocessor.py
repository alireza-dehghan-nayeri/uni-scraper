import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def convert_lowercase(text):
    return text.lower()


def remove_numbers(text):
    result = re.sub(r'\d+', '', text)
    return result


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def remove_whitespace(text):
    return ' '.join(text.split())


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [
        word for word in word_tokens if word not in stop_words]
    removed_stopwords = ''
    for word in filtered_text:
        removed_stopwords += word + ' '
    return removed_stopwords


def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    stemmed_words = ''
    for word in stems:
        stemmed_words += word + ' '
    return stemmed_words


def lemmatize_word(text):
    word_tokens = word_tokenize(text)
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in word_tokens]
    lemmatized_words = ''
    for word in lemmas:
        lemmatized_words += word + ' '
    return lemmatized_words


def preprocess(text):
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = convert_lowercase(text)
    text = remove_whitespace(text)
    text = remove_stopwords(text)
    text = remove_whitespace(text)
    text = stem_words(text)
    text = remove_whitespace(text)
    text = lemmatize_word(text)
    text = remove_whitespace(text)
    return text
