import oracledb
import os
from Application.objects.competency import Competency

from Application.objects.course import Course
from Application.objects.element import Element

class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []
                        
    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def __get_cursor(self):
            for i in range(3):
                try:
                    return self.__connection.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()
                    
    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()

    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                             host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")

    def get_all_courses(self):
        with self.__get_cursor() as cursor:
            all_courses = []

            try:
                results = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses""")

                for row in results:
                    course = Course(row[1], row[2], row[3], row[4], row[5], row[6])
                    course.id = row[0]
                    all_courses.append(course)

            except oracledb.Error:
                pass

            return all_courses

    def get_course(self, id):
        # if not isinstance(id, int):
        #     raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            try:
                result = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses WHERE course_id=:id""", id=id)
                
                for row in result:
                    course = Course(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    course.id = row[0]
                    return course
                
            except oracledb.Error:
                pass

    def get_course_competencies(self, id):
        # if not isinstance(id, int):
        #     raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            all_course_competencies = []

            try:
                results = cursor.execute("""SELECT competency_id, competency, competency_achievement, 
                competency_type FROM view_courses_elements_competencies WHERE course_id=:id""", id=id)

                for row in results:
                    competency = Competency(row[1], row[2], row[3])
                    competency.id = row[0]
                    all_course_competencies.append(competency)

            except oracledb.Error:
                pass

            return all_course_competencies

    def get_competency_elements(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            all_competency_elements = []

            try:
                results = cursor.execute("""SELECT element_id, element_order, element, element_criteria 
                FROM view_competencies_elements WHERE competency_id=:id""", id=id)

                for row in results:
                    element = Element(row[1], row[2], row[3])
                    element.id = row[0]
                    all_competency_elements.append(element)

            except oracledb.Error:
                pass

            return all_competency_elements

    def get_courses_by_term(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            all_courses_by_term = []

            try:
                results = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours, 
                work_hours, description, domain_id, term_id FROM view_courses_terms WHERE term_id=:id"""
                                         , id=id)
                
                for row in results:
                    course = Course(row[1], row[2], row[3], row[4], row[5], row[6])
                    course.id = row[0]
                    all_courses_by_term.append(course)
                
            except oracledb.Error:
                pass

            return all_courses_by_term

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')