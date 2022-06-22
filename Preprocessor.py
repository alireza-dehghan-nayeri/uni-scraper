import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


class Preprocessor:

    def __init__(self):
        pass

    def preprocess(self, text):
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.convert_lowercase(text)
        text = self.remove_whitespace(text)
        text = self.remove_stopwords(text)
        text = self.remove_whitespace(text)
        text = self.stem_words(text)
        text = self.remove_whitespace(text)
        text = self.lemmatize_word(text)
        text = self.remove_whitespace(text)
        return text

    def convert_lowercase(self, text):
        return text.lower()

    def remove_numbers(self, text):
        result = re.sub(r'\d+', '', text)
        return result

    def remove_punctuation(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def remove_whitespace(self, text):
        return ' '.join(text.split())

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [
            word for word in word_tokens if word not in stop_words]
        removed_stopwords = ''
        for word in filtered_text:
            removed_stopwords += word + ' '
        return removed_stopwords

    def stem_words(self, text):
        word_tokens = word_tokenize(text)
        stems = [stemmer.stem(word) for word in word_tokens]
        stemmed_words = ''
        for word in stems:
            stemmed_words += word + ' '
        return stemmed_words

    def lemmatize_word(self, text):
        word_tokens = word_tokenize(text)
        # provide context i.e. part-of-speech
        lemmas = [lemmatizer.lemmatize(word, pos='v') for word in word_tokens]
        lemmatized_words = ''
        for word in lemmas:
            lemmatized_words += word + ' '
        return lemmatized_words
