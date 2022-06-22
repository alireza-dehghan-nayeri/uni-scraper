import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

te = TransactionEncoder()


class FrequentPatternExtractor:
    def __init__(self):
        pass

    def extractFrequentPatternsAndAssosiationRules(self, keywords_dic):
        # frequent patterns and association rules
        te_ary = te.fit(keywords_dic.values()).transform(keywords_dic.values())
        df = pd.DataFrame(te_ary, columns=te.columns_)
        df.to_csv('data-out/departments-courses-details-keywords-data.csv')

        frequent_items = apriori(df, min_support=0.01, use_colnames=True)
        # print(frequent_items)
        frequent_items.to_csv('data-out/frequent-patterns-data.csv')

        rules = association_rules(
            frequent_items, metric='confidence', min_threshold=0.01)
        # print(rules)
        rules.to_csv('data-out/rules-data.csv')
