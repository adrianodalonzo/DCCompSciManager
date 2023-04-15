import oracledb
import os
from Application.objects.competency import Competency
from Application.objects.course import Course
from Application.objects.domain import Domain
from Application.objects.element import Element
from .objects.user import User

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
            
    def insert_user(self, user):
        if not isinstance(user, User):
            raise TypeError('User passed in MUST be a User object!')
        
        with self.__get_cursor() as cursor:
            cursor.execute("""select email from courses_users where email = :email""", email=user.email)
            if cursor.rowcount != 0:
                raise oracledb.IntegrityError
        
        with self.__get_cursor() as cursor:
            cursor.execute("""insert into courses_users (username, email, password, user_group, avatar_path) 
                           values (:username, :email, :password, 'Member', :avatar_path)""",
                           username=user.name, 
                           email=user.email, 
                           password=user.password,
                           avatar_path=user.avatarlink)
            
    def get_user(self, email):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')

        with self.__get_cursor() as cursor:
            results = cursor.execute("""select email, password, user_id, username, user_group, avatar_path from courses_users
                                     where email = :email""", email=email)
            for result in results:
                user = User(result[0], result[3], result[1], result[5])
                user.id = result[2]
                user.group = result[4]
                return user
            
    def get_user_id(self, id):
        if not isinstance(id, int):
            raise TypeError('ID MUST be a number!!')
        
        with self.__get_cursor() as cursor:
            results = cursor.execute("""select email, password, user_id, username, user_group, avatar_path from courses_users
                                     where user_id = :id""", id=id)
            for result in results:
                user = User(result[0], result[3], result[1], result[5])
                user.id = result[2]
                user.group = result[4]
                return user

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
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    all_courses.append(course)

            except oracledb.Error:
                pass

            return all_courses

    def get_course(self, id):  
        with self.__get_cursor() as cursor:
            try:
                result = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses WHERE course_id=:id""", id=id)
                
                for row in result:
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    return course
                
            except oracledb.Error:
                pass
    
    def add_course(self, course):
        if self.get_course(course.id):
            raise ValueError("Course already exist. Please change to a valid course ID.") 
            
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO courses VALUES(:id, :title, :theory_hours, :lab_hours, :work_hours, :description, :domain_id, :term_id)",
                    id=course.id, title=course.title, theory_hours=course.theory_hours, lab_hours=course.lab_hours,
                    work_hours=course.work_hours, description=course.description, domain_id=course.domain_id, term_id=course.term_id)
    
    def modify_course(self, course):
        if not self.get_course(course.id):
            raise ValueError("Course does not exist. Please modify an existing course.") 
            
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATES courses SET course_title=:course_title, theory_hours=:theory_hours, lab_hours=:lab_hours, work_hours=:work_hours, description=:description, domain_id:domain_id, term_id:term_id WHERE course_id=:course_id)",
                    course_id=course.id, course_title=course.title, theory_hours=course.theory_hours, lab_hours=course.lab_hours,
                    work_hours=course.work_hours, description=course.description, domain_id=course.domain_id, term_id=course.term_id)):

    def delete_course(self, id):
        if not self.get_course(course.id):
            raise ValueError("Course does not exist. Please choose an existing course to delete.") 

        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM courses WHERE course_id=:course_id)", course_id=course.id):

    def get_course_competencies(self, id): 
        with self.__get_cursor() as cursor:
            all_course_competencies = []

            try:
                results = cursor.execute("""SELECT competency_id, competency, competency_achievement, 
                competency_type FROM view_courses_elements_competencies WHERE course_id=:id""", id=id)

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    all_course_competencies.append(competency)

            except oracledb.Error:
                pass

            return all_course_competencies

    def get_competency(self, id):
         with self.__get_cursor() as cursor:

            try:
                results = cursor.execute("""SELECT competency_id, competency, competency_achievement, 
                competency_type FROM competencies WHERE competency_id=:id""", id=id)

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    return competency
            
            except oracledb.Error:
                pass
    
    def get_all_competencies(self):
        with self.__get_cursor() as cursor:
            all_competencies = []

            try:
                results = cursor.execute("""SELECT competency_id, competency, competency_achievement, 
                competency_type FROM competencies""")

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    all_competencies.append(competency)
                
            except oracledb.Error:
                pass

        return all_competencies

    def add_competency(self, competency):
        if self.get_competency(competency.id):
            raise ValueError("Competency already exist. Please modify an existing competency.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATES competencies SET competency=:competency, competency_achievement=:competency_achievement, competency_type=:competency_type WHERE competency_id=:competency_id",
                           competency_id=competency.id, competency=competency.name, competency_achievement=competency.achievement, competency_type=competency.type)
    
    def modify_competency(self, competency):
        if not self.get_competency(competency.id):
            raise ValueError("Competency does not exist. Please change to a valid competency id.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO competencies VALUES(:competency_id, :competency, :competency_achievement, :competency_type FROM competencies WHERE competency_id=:id)",
                           competency_id=competency.id, competency=competency.name, competency_achievement=competency.achievement, competency_type=competency.type)

     def delete_competency(self, id):
        if not self.get_competency(id):
            raise ValueError("Competency does not exist. Please choose an existing competency to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM competencies WHERE competency_id=:competency_id)", competency_id=competency.id)

    def get_competency_elements(self, id):
        with self.__get_cursor() as cursor:
            all_competency_elements = []

            try:
                results = cursor.execute("""SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM view_competencies_elements WHERE competency_id=:id""", id=id)

                for row in results:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    all_competency_elements.append(element)

            except oracledb.Error:
                pass

            return all_competency_elements

    def add_competency_element(self, element):
        if self.get_competency_elements(element.competency_id).name == element.name:
            raise ValueError("Element already exist in this competency. Please change the element order.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO elements VALUES(:element_order, :element, :element_criteria, :competency_id)",
            element_order=element.order, element=element.name, element_criteria=element.criteria, competency_id=element.competency_id)

    def modify_competency_element(self, element):
        if not (self.get_competency_elements(element.competency_id).name == element.name):
            raise ValueError("Element does not exist in this competency. Please modify an existing competency element.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATE elements SET element_order=:element_order, element=:element, element_criteria=:element_criteria, competency_id:competency_id WHERE element=:element)",
            element_order=element.order, element=element.name, element_criteria=element.criteria, competency_id=element.competency_id)

    def delete_competency_element(self, element):
        if not (self.get_competency_elements(element.competency_id).name == element.name):
            raise ValueError("Element does not exist in this competency. Please choose an existing competency element to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM elements WHERE element_order=:element_order AND competency_id=:competency_id)",
            element_order=element.order, competency_id=element.competency_id)

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
                    course = Course(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    course.id = row[0]
                    all_courses_by_term.append(course)
                
            except oracledb.Error:
                pass

            return all_courses_by_term
        
    def get_domain(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            try:
                result = cursor.execute("""SELECT domain, domain_description FROM domains
                WHERE domain_id=:id""", id=id)

                for row in result:
                    domain = Domain(row[0], row[1])
                    domain.id = id
                    return domain
                
            except oracledb.Error:
                pass
    
    def get_courses_by_domain(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            courses_by_domain = []

            try:
                results = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours, 
                work_hours, description, term_id FROM view_courses_domains WHERE domain_id=:id"""
                                         , id=id)

                for row in results:
                    course = Course(row[1], row[2], row[3], row[4], row[5], id, row[6])
                    course.id = row[0]
                    courses_by_domain.append(course)

            except oracledb.Error:
                pass

            return courses_by_domain
        
    def get_all_domains(self):
        with self.__get_cursor() as cursor:
            all_domains = []

            try:
                results = cursor.execute("""SELECT domain_id, domain, domain_description 
                FROM domains""")

                for row in results:
                    domain = Domain(row[1], row[2])
                    domain.id = row[0]
                    all_domains.append(domain)

            except oracledb.Error:
                pass

            return all_domains
    
    def add_domain(self, domain):
        if self.get_domain(domain.id):
            raise ValueError("Domain already exist. Please change the domain id.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO domains VALUES(:domain, :domain_description)",
            domain=domain.name, domain_description=domain.description)

    def modify_domain(self, domain):
        if not self.get_domain(domain.id):
            raise ValueError("Domain does not exist. Please modify an existing domain.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATE domains domain=:domain, domain_description=:domain_description)",
            domain=domain.name, domain_description=domain.description)

    def delete_domain(self, domain):
        if not self.get_domain(domain.id):
            raise ValueError("Domain does not exist. Please choose an existing domain to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM domains WHERE domain_id=:domain_id)", domain=domain.id)

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')