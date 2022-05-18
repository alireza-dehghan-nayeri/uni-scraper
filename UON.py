from BaseCrawler import BaseCrawler
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('__main__')


class UON(BaseCrawler):

    Course_Page_Url = 'https://www.newcastle.edu.au/course'
    University = 'The University of Newcastle, Australia'
    Abbreviation = 'UON'
    University_Homepage = 'https://www.newcastle.edu.au/'

    # Below fields didn't find in the website
    References = None
    Projects = None
    Professor_Homepage = None
    Professor = None

    def get_courses_of_department(self, department):

        theads = department.find_elements(By.TAG_NAME, 'thead')
        Department_Name = ''
        for thead in theads:
            if len(thead.text.split()) != 0:
                temp = thead.text.split()[1:]
                Department_Name = ' '.join(str(item) for item in temp)

        courses = department.find_elements(By.CLASS_NAME, 'title')

        return courses, Department_Name

    def get_course_data(self, course):

        Course_Title = course.text
        Course_Homepage = course.find_element(
            By.TAG_NAME, 'a').get_attribute('href')

        course_page_content = requests.get(Course_Homepage).text
        course_soup = BeautifulSoup(course_page_content, 'html.parser')

        sections = course_soup.find_all(class_='fast-fact-item')
        Unit = ''
        if sections is not None:
            for section in sections:
                if section.find('strong').text == 'Units':
                    Unit = section.find('p').text

        description = ''
        if course_soup.find(id='course-details') is not None:
            des = course_soup.find(
                id='course-details').find(id='description')
            while des.next_sibling.name == 'p':
                description = description+'\n'+des.next_sibling.text
                des = des.next_sibling

        content = ''
        if course_soup.find(id='course-details') is not None:
            content0 = course_soup.find(
                id='course-details').find(id='coursecontent')
            while content0.next_sibling.name == 'p' or content0.next_sibling.name == 'ul':
                content = content+'\n'+content0.next_sibling.text
                content0 = content0.next_sibling

        outcome = ''
        if course_soup.find(id='course-details') is not None:
            mid1 = course_soup.find(
                id='course-details').find(id='learningoutcomes')
            while mid1.next_sibling.name == 'p':
                outcome = outcome+'\n'+mid1.next_sibling.text
                mid1 = mid1.next_sibling

        assumed_knowledge = ''
        if course_soup.find(id='course-details') is not None:
            mid2 = course_soup.find(
                id='course-details').find(id='assumedknowledge')
            if mid2 != None:
                while mid2.next_sibling.name == 'p':
                    assumed_knowledge = assumed_knowledge+'\n'+mid2.next_sibling.text
                    mid2 = mid2.next_sibling

        requisite = ''
        if course_soup.find(id='course-details') is not None:
            mid3 = course_soup.find(
                id='course-details').find(id='requisite')
            if mid3 != None:
                while mid3.next_sibling.name == 'p':
                    requisite = requisite+'\n'+mid3.next_sibling.text
                    mid3 = mid3.next_sibling

        assessment = ''
        if course_soup.find(id='course-details') is not None:
            mid4 = course_soup.find(
                id='course-details').find(id='assessmentitems')
            if mid4 != None:
                while mid4.next_sibling is not None and mid4.next_sibling.name == 'p':
                    assessment = assessment+'\n'+mid4.next_sibling.text
                    mid4 = mid4.next_sibling

        return Course_Title, Course_Homepage, Unit, description, outcome, assumed_knowledge, requisite, content, assessment

    def handler(self):

        driver = webdriver.Firefox()
        driver.get('https://www.newcastle.edu.au/course')

        departments = driver.find_elements(By.TAG_NAME, 'table')

        for department in departments:
            courses, Department_Name = self.get_courses_of_department(
                department)
            #print(courses, Department_Name)

            for course in courses:
                Course_Title, Course_Homepage, Unit_Count, Description, Outcome, Required_Skills, Prerequisite, Objective, Scores = self.get_course_data(
                    course)
                # print(Scores)
                self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    self.Professor, Objective, Prerequisite, Required_Skills, Outcome, self.References, Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )

            logger.info(
                f"{self.Abbreviation}: {Department_Name} department's data was crawled successfully.")

        logger.info(
            f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")

        driver.quit()


uon = UON()
uon.handler()
