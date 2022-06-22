from keybert import KeyBERT

kw_model = KeyBERT()


class KeywordsExtractor:

    def __init__(self):
        pass

    def extract_keyword(self, text):
        final_keyword_list = []
        bert_generated_keywords = kw_model.extract_keywords(text)
        for keyword in bert_generated_keywords:
            final_keyword_list.append(keyword[0])
        return final_keyword_list
