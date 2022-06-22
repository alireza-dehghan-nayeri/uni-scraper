import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from BaseCrawler import BaseCrawler

logger = logging.getLogger('__main__')


class UON(BaseCrawler):
    Course_Page_Url = 'https://www.newcastle.edu.au/course'
    University = 'The University of Newcastle, Australia'
    Abbreviation = 'UON'
    University_Homepage = 'https://www.newcastle.edu.au/'

    # Below fields were not found in the website
    References = None
    Projects = None
    Professor_Homepage = None
    Professor = None

    def get_courses_of_department(self, department):

        t_heads = department.find_elements(By.TAG_NAME, 'thead')
        department_name = ''
        for thead in t_heads:
            if len(thead.text.split()) != 0:
                temp = thead.text.split()[1:]
                department_name = ' '.join(str(item) for item in temp)

        courses = department.find_elements(By.CLASS_NAME, 'title')

        return courses, department_name

    def get_course_data(self, course):

        course_title = course.text
        course_homepage = course.find_element(
            By.TAG_NAME, 'a').get_attribute('href')

        course_page_content = requests.get(course_homepage).text
        course_soup = BeautifulSoup(course_page_content, 'html.parser')

        sections = course_soup.find_all(class_='fast-fact-item')
        unit = ''
        if sections is not None:
            for section in sections:
                if section.find('strong').text == 'Units':
                    unit = section.find('p').text

        description = ''
        if course_soup.find(id='course-details') is not None:
            des = course_soup.find(
                id='course-details').find(id='description')
            while des.next_sibling.name == 'p':
                description = description + '\n' + des.next_sibling.text
                des = des.next_sibling

        content = ''
        if course_soup.find(id='course-details') is not None:
            content0 = course_soup.find(
                id='course-details').find(id='coursecontent')
            while content0.next_sibling.name == 'p' or content0.next_sibling.name == 'ul':
                content = content + '\n' + content0.next_sibling.text
                content0 = content0.next_sibling

        outcome = ''
        if course_soup.find(id='course-details') is not None:
            mid1 = course_soup.find(
                id='course-details').find(id='learningoutcomes')
            while mid1.next_sibling.name == 'p':
                outcome = outcome + '\n' + mid1.next_sibling.text
                mid1 = mid1.next_sibling

        assumed_knowledge = ''
        if course_soup.find(id='course-details') is not None:
            mid2 = course_soup.find(
                id='course-details').find(id='assumedknowledge')
            if mid2 is not None:
                while mid2.next_sibling.name == 'p':
                    assumed_knowledge = assumed_knowledge + '\n' + mid2.next_sibling.text
                    mid2 = mid2.next_sibling

        requisite = ''
        if course_soup.find(id='course-details') is not None:
            mid3 = course_soup.find(
                id='course-details').find(id='requisite')
            if mid3 is not None:
                while mid3.next_sibling.name == 'p':
                    requisite = requisite + '\n' + mid3.next_sibling.text
                    mid3 = mid3.next_sibling

        assessment = ''
        if course_soup.find(id='course-details') is not None:
            mid4 = course_soup.find(
                id='course-details').find(id='assessmentitems')
            if mid4 is not None:
                while mid4.next_sibling is not None and mid4.next_sibling.name == 'p':
                    assessment = assessment + '\n' + mid4.next_sibling.text
                    mid4 = mid4.next_sibling

        return (
            course_title,
            course_homepage,
            unit, description,
            outcome,
            assumed_knowledge,
            requisite,
            content,
            assessment
        )

    def handler(self):

        driver = webdriver.Firefox()
        driver.get('https://www.newcastle.edu.au/course')

        departments = driver.find_elements(By.TAG_NAME, 'table')

        for department in departments:
            courses, department_name = self.get_courses_of_department(
                department)

            for course in courses:
                (
                    course_title,
                    course_homepage,
                    unit_count,
                    description,
                    outcome,
                    required_skills,
                    prerequisite,
                    objective,
                    scores
                ) = self.get_course_data(course)

                self.save_course_data(
                    self.University,
                    self.Abbreviation,
                    department_name,
                    course_title,
                    unit_count,
                    self.Professor,
                    objective,
                    prerequisite,
                    required_skills,
                    outcome,
                    self.References,
                    scores,
                    description,
                    self.Projects,
                    self.University_Homepage,
                    course_homepage,
                    self.Professor_Homepage
                )

            logger.info(
                f"{self.Abbreviation}: {department_name} department's data was crawled successfully.")

        logger.info(
            f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")

        driver.quit()


uon = UON()
uon.handler()
