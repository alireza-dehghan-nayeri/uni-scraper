import csv

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

from FrequentPatternExtractor import extract_frequent_patterns_and_association_rules
from KeywordsExtractor import extract_keyword
from Preprocessor import preprocess

plt.rcParams["figure.figsize"] = (15, 8)
keywords_dic = dict()

# load the main data
data = pd.read_csv('data-in/UON.csv')

# count number of all courses and courses of each department
courses_count = len(data.index)
departments_count = len(data.groupby('Department'))
department_courses_count = data.groupby('Department')['Course title'].count()

statistic_comparison = csv.writer(
    open(f'data-out/departments-courses-count-comparison-data.csv', 'w', encoding='utf-8', newline=''))
statistic_comparison.writerow(['Department', 'CoursesCount', 'Comparison'])

avg = int(courses_count / departments_count)

for department, course_count in department_courses_count.items():
    if int(course_count) == avg:
        statistic_comparison.writerow(
            [department, course_count, 'equal'])
    elif int(course_count) > avg:
        statistic_comparison.writerow(
            [department, course_count, 'more than average'])
    else:
        statistic_comparison.writerow(
            [department, course_count, 'less than average'])

# visualization
department_courses_count.to_csv(
    'data-out/visualization-data.csv', header=False)

departments = []
departments_courses_count = []

with open('data-out/visualization-data.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        departments.append(row[0])
        departments_courses_count.append(int(row[1]))

plt.scatter(departments, departments_courses_count)
plt.xticks(rotation=90, fontsize=5)
plt.ylabel('Courses Count')
plt.tick_params(axis="x", pad=10)
plt.xlabel('Department Name')
plt.tight_layout()
plt.savefig('data-out/departments-courses-count-chart.png', dpi=400)

# add a new col which consists of course title,objective,outcome and description of each course
data['Courses Detail'] = data['Course title'] + \
                         data['Objective'] + data['Outcome'] + data['Description']

# group data by department and its courses and their details
department_data = data.groupby('Department')['Courses Detail'].sum()
department_data.to_csv('data-out/departments-and-courses-details-data.csv')

# preprocess and extract keywords
output_file = csv.writer(
    open(f'data-out/department-and-courses-details-preprocessed-data.csv', 'w', encoding='utf-8', newline=''))
output_file.writerow(['Department', 'Courses Detail'])

for department, courses_detail in department_data.items():
    if type(courses_detail) == int:
        courses_detail = ''
    preprocessed_courses_detail = preprocess(courses_detail)
    print(department + '-> preprocessed courses detail')
    output_file.writerow(
        [department, preprocessed_courses_detail])

    keywords_dic[department] = extract_keyword(
        preprocessed_courses_detail)
    print(department + '-> extracted courses detail keywords')

# WordCloud
all_keywords = []
for value in keywords_dic.values():
    for key in value:
        all_keywords.append(key)
print(all_keywords)
keyword_string = " ".join(all_keywords)
print(keyword_string)
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      min_font_size=10).generate(keyword_string)

# plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('data-out/keywords-word-cloud-chart.png', dpi=400)
# frequent patterns and association rules
extract_frequent_patterns_and_association_rules(
    keywords_dic)
