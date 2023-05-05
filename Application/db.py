import oracledb
import os
from Application.objects.competency import Competency
from Application.objects.course import Course
from Application.objects.domain import Domain
from Application.objects.element import Element
from Application.objects.term import Term
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
            
    def insert_user(self, user, group=None):
        if not isinstance(user, User):
            raise TypeError('User passed in MUST be a User object!')
        
        with self.__get_cursor() as cursor:
            cursor.execute("""select email from courses_users where email = :email""", email=user.email)
            if cursor.rowcount != 0:
                raise oracledb.IntegrityError
        
        with self.__get_cursor() as cursor:
            query_string = ""
            if group is None:
                query_string = """insert into courses_users (username, email, password, user_group, blocked) 
                           values (:username, :email, :password, 'Member', '0')"""
                cursor.execute(query_string, username=user.name, email=user.email, password=user.password)
            else:
                query_string = """insert into courses_users (username, email, password, user_group, blocked) 
                           values (:username, :email, :password, :user_group, '0')"""
                cursor.execute(query_string, username=user.name, email=user.email, password=user.password, user_group=group)
                
    
    def fetch_blocked(result):
        if result == '1':
            return True
        return False
    
    def get_users(self):
        users = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('select email, password, user_id, username, user_group, blocked from courses_users')

            for result in results:
                user = User(result[0], result[3], result[1])
                user.id = result[2]
                user.group = result[4]
                user.blocked = Database.fetch_blocked(result[5])
                users.append(user)
        return users
            
    def get_user(self, email):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')

        with self.__get_cursor() as cursor:
            results = cursor.execute("""select email, password, user_id, username, user_group, blocked from courses_users
                                     where email = :email""", email=email)
            for result in results:
                user = User(result[0], result[3], result[1])
                user.id = result[2]
                user.group = result[4]
                user.blocked = Database.fetch_blocked(result[5])
                return user
            
    def get_user_id(self, id):
        if not isinstance(id, int):
            raise TypeError('ID MUST be a number!!')
        
        with self.__get_cursor() as cursor:
            results = cursor.execute("""select email, password, user_id, username, user_group, blocked from courses_users
                                     where user_id = :id""", id=id)
            for result in results:
                user = User(result[0], result[3], result[1])
                user.id = result[2]
                user.group = result[4]
                user.blocked = Database.fetch_blocked(result[5])
                return user
            
    def update_user_password(self, email, password):
        if not isinstance(password, str):
            raise TypeError('Password MUST be a string!')
        
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        with self.__get_cursor() as cursor:
            user_id = self.get_user(email).id
            cursor.execute('update courses_users set password = :password where user_id = :id', password=password, id=user_id)

    def update_user_username(self, email, username):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        if not isinstance(username, str):
            raise TypeError('Username MUST be a string!')
        
        with self.__get_cursor() as cursor:
            cursor.execute('update courses_users set username = :username where email = :email', username=username, email=email)
            
    def get_members(self):
        members = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Member'")
            for result in results:
                member = User(result[0], result[3], result[1])
                member.id = result[2]
                member.group = result[4]
                member.blocked = Database.fetch_blocked(result[5])
                members.append(member)
        return members
    
    def get_user_admins(self):
        user_admins = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'User Admin'")
            for result in results:
                user_admin = User(result[0], result[3], result[1])
                user_admin.id = result[2]
                user_admin.group = result[4]
                user_admin.blocked = Database.fetch_blocked(result[5])
                user_admins.append(user_admin)
        return user_admins
    
    def get_admins(self):
        admins = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Admin'")
            for result in results:
                admin = User(result[0], result[3], result[1])
                admin.id = result[2]
                admin.group = result[4]
                admin.blocked = Database.fetch_blocked(result[5])
                admins.append(admin)
        return admins
    
    def get_unblocked_members(self):
        members = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Member' and blocked = '0'")
            for result in results:
                member = User(result[0], result[3], result[1])
                member.id = result[2]
                member.group = result[4]
                member.blocked = Database.fetch_blocked(result[5])
                members.append(member)
        return members
    
    def get_blocked_members(self):
        members = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Member' and blocked = '1'")
            for result in results:
                member = User(result[0], result[3], result[1])
                member.id = result[2]
                member.group = result[4]
                member.blocked = Database.fetch_blocked(result[5])
                members.append(member)
        return members
    
    def delete_user(self, email):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        with self.__get_cursor() as cursor:
            cursor.execute('delete from courses_users where email = :email', email=email)
            
    def block_member(self, email):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        with self.__get_cursor() as cursor:
            cursor.execute("update courses_users set blocked = '1' where email = :email", email=email)
            
    def unblock_member(self, email):
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        with self.__get_cursor() as cursor:
            cursor.execute("update courses_users set blocked = '0' where email = :email", email=email)

    def move_member(self, email, group):
        if not isinstance(email, str):
            raise TypeError("Email MUST be a string!")
        
        if not isinstance(group, str):
            raise TypeError("Email MUST be a string!")
        
        with self.__get_cursor() as cursor:
            cursor.execute('update courses_users set user_group = :user_group where email = :email', user_group=group, email=email)

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

    def get_all_courses(self, page_num=1, page_size=5):
        all_courses = []
        prev_page = None
        next_page = None
        offset = (page_num - 1)*page_size
        with self.__get_cursor() as cursor:
            try:
                results = cursor.execute("""SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses ORDER BY course_id OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY""", offset=offset, page_size=page_size)

                for row in results:
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    all_courses.append(course)
                
                if page_num > 1:
                    prev_page = page_num - 1
                if len(all_courses) > 0 and (len(all_courses) >= page_size):
                    next_page = page_num + 1
                
                return all_courses, prev_page, next_page

            except oracledb.Error:
                pass

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
                    (course.id, course.title, course.theory_hours, course.lab_hours, course.work_hours, 
                     course.description, course.domain_id, course.term_id))
    
    def modify_course(self, course):
        if not self.get_course(course.id):
            raise ValueError("Course does not exist. Please modify an existing course.") 
            
        with self.__connection.cursor() as cursor:
            cursor.execute("""UPDATE courses SET course_title=:course_title, theory_hours=:theory_hours, lab_hours=:lab_hours, work_hours=:work_hours, 
            description=:description, domain_id=:domain_id, term_id=:term_id WHERE course_id=:course_id""",
                    (course.title, course.theory_hours, course.lab_hours, course.work_hours, 
                     course.description, course.domain_id, course.term_id, course.id))

    def delete_course(self, id):
        if not self.get_course(id):
            raise ValueError("Course does not exist. Please choose an existing course to delete.") 

        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM courses WHERE course_id=:course_id", course_id=id)

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
    
    def get_all_competencies(self, page_num=1, page_size=5):
        all_competencies = []
        prev_page = None
        next_page = None
        offset = (page_num - 1) * page_size
        with self.__get_cursor() as cursor:
            try:
                results = cursor.execute("""SELECT competency_id, competency, competency_achievement, 
                competency_type FROM competencies ORDER BY competency_id OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY""", offset=offset, page_size=page_size)

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    all_competencies.append(competency)
                    
                if page_num > 1:
                    prev_page = page_num - 1
                if len(all_competencies) > 0 and (len(all_competencies) >= page_size):
                    next_page = page_num + 1
                
                return all_competencies, prev_page, next_page
                        
            except oracledb.Error:
                pass

    def add_competency(self, competency):
        if self.get_competency(competency.id):
            raise ValueError("Competency already exist. Please modify an existing competency.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO competencies VALUES(:competency_id, :competency, :competency_achievement, :competency_type)",
                           (competency.id, competency.name, competency.achievement, competency.type))
          
    def modify_competency(self, competency):
        if not self.get_competency(competency.id):
            raise ValueError("Competency does not exist. Please change to a valid competency id.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATE competencies SET competency=:competency, competency_achievement=:competency_achievement, competency_type=:competency_type WHERE competency_id=:competency_id",
                           (competency.name, competency.achievement, competency.type, competency.id))
    
    def delete_competency(self, id):
        if not self.get_competency(id):
            raise ValueError("Competency does not exist. Please choose an existing competency to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM competencies WHERE competency_id=:competency_id", competency_id=id)

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


    def get_competency_element(self, competency_id, element_id):
        if not isinstance(element_id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            try:
                result = cursor.execute("""SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM elements WHERE competency_id=:compentecy_id AND element_id=:element_id""", (competency_id, element_id))

                for row in result:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    return element

            except oracledb.Error:
                pass
    
    def get_all_elements(self):
        elements = []
        
        with self.__get_cursor() as cursor:
            try:
                results = cursor.execute("""SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM elements""")

                for row in results:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    elements.append(element)
                    
                return elements    
            
            except oracledb.Error:
                pass
            
    def get_element(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        
        with self.__get_cursor() as cursor:
            try:
                result = cursor.execute("""SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM elements WHERE element_id=:id""", id=id)

                for row in result:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    return element
                
            except oracledb.Error:
                pass
        
    def get_last_element_id(self):
        with self.__get_cursor() as cursor:
            result = cursor.execute("SELECT element_id FROM elements WHERE element_id = (SELECT MAX(element_id) FROM elements)")
            for row in result:
                element_id = int(row[0])
                return element_id

    def get_element_by_both_id(self, course_id, elem_id):
        with self.__get_cursor() as cursor:
            try:
                hours_query = cursor.execute("""SELECT element_hours FROM courses_elements WHERE element_id=:elem_id
                AND course_id=:course_id""", (elem_id, course_id))

                for row in hours_query:
                    hours = row[0]

                result = cursor.execute("""SELECT element_order, element, element_criteria, competency_id 
                    FROM view_competencies_elements WHERE element_id=:id""", id=elem_id)
                
                for row in result:
                        element = Element(row[0], row[1], row[2], row[3])
                        element.id = id
                        element.hours = hours
                        return element
                
            except oracledb.Error:
                pass

    def add_competency_element(self, element):
        competency_elements = self.get_competency_elements(element.competency_id)
        for competency_element in competency_elements:
            if competency_element.name == element.name:
                raise ValueError("Element already exist in this competency. Please change the element order.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO elements (element_order, element, element_criteria, competency_id) VALUES(:element_order, :element, :element_criteria, :competency_id)",
                           (element.order, element.name, element.criteria, element.competency_id))

    def modify_competency_element(self, element):
        competency_elements = self.get_competency_elements(element.competency_id)
        element_exist = False
        for competency_element in competency_elements:
            if competency_element.id == element.id:
                element_exist = True

        if not element_exist:
            raise ValueError("Element does not exist in this competency. Please modify an existing competency element.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("""UPDATE elements SET element_order=:element_order, element=:element, 
            element_criteria=:element_criteria, competency_id=:competency_id WHERE element_id=:element_id""", 
            (element.order, element.name, element.criteria, element.competency_id, element.id))

    def delete_competency_element(self, element):
        competency_elements = self.get_competency_elements(element.competency_id)
        element_exist = False
        for competency_element in competency_elements:
            if competency_element.name == element.name:
                element_exist = True

        if not element_exist:
            raise ValueError("Element does not exist in this competency. Please choose an existing competency element to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM elements WHERE element_order=:element_order AND competency_id=:competency_id",
                           (element.order, element.competency_id))

    def get_course_elements(self, course_id):
        if not isinstance(course_id, str):
            raise TypeError("course_id must be a string")
        
        with self.__get_cursor() as cursor:
            course_elements = []
            try:

                elements = cursor.execute("""SELECT element_id, element_hours, element_order, element, element_criteria,
                competency_id FROM view_courses_elements WHERE course_id=:course_id""", course_id=course_id)
                
                for row in elements:
                    element = Element(row[2], row[3], row[4], row[5])
                    element.id = row[0]
                    element.hours = row[1]
                    course_elements.append(element)

            except oracledb.Error:
                pass
            
            return course_elements
    
    def get_all_elements(self):
        all_elements = []

        with self.__get_cursor() as cursor:
            try:
                elements = cursor.execute("SELECT element_id, element FROM elements")

                for row in elements:
                    all_elements.append((row[0], row[1]))
            
            except oracledb.Error:
                pass

        return all_elements
    
    def add_course_element(self, course_id, elem_id, hours):
        if not isinstance(course_id, str):
            raise TypeError("course_id must be a string")
        if not isinstance(elem_id, str):
            raise TypeError("elem_id must be a string")
        if not isinstance(hours, int):
            raise TypeError("hours must be an int")

        with self.__get_cursor() as cursor:
            try:
                cursor.execute("INSERT INTO courses_elements VALUES(:course_id, :element_id, :element_hours)",
                                (course_id, elem_id, hours))
            except oracledb.Error:
                pass
    
    def edit_course_element(self, course_id, elem_id, hours):
        if not isinstance(course_id, str):
            raise TypeError("course_id must be a string")
        if not isinstance(elem_id, str):
            raise TypeError("elem_id must be a string")
        if not isinstance(hours, int):
            raise TypeError("hours must be an int")
        
        with self.__get_cursor() as cursor:
            try:
                cursor.execute("""UPDATE courses_elements SET element_hours=:hours WHERE course_id=:course_id
                AND element_id=:elem_id""", (hours, course_id, elem_id))
            except oracledb.Error:
                pass
        
    def delete_course_element(self, course_id, elem_id):
        if not isinstance(course_id, str):
            raise TypeError("course_id must be a string")
        if not isinstance(elem_id, str):
            raise TypeError("elem_id must be a string")
        
        with self.__get_cursor() as cursor:
            try:
                cursor.execute("DELETE FROM courses_elements WHERE course_id=:course_id AND element_id=:elem_id"
                                , (course_id, elem_id))
            except oracledb.Error:
                pass

    def get_all_terms(self):
        with self.__get_cursor() as cursor:
            all_terms = []
            try:
                results = cursor.execute("SELECT term_id, term_name FROM terms")

                for row in results:
                    term = Term(row[1])
                    term.id = row[0]
                    all_terms.append(term)

            except oracledb.Error:
                pass

            return all_terms

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
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
                return None

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
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], id, row[6])
                    courses_by_domain.append(course)

            except oracledb.Error:
                pass

            return courses_by_domain
        
    def get_all_domains(self, page_num=1, page_size=5):
        all_domains = []
        prev_page = None
        next_page = None
        offset = (page_num - 1) * page_size
        with self.__get_cursor() as cursor:
            try:
                results = cursor.execute("""SELECT domain_id, domain, domain_description 
                FROM domains ORDER BY domain_id OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY""", offset=offset, page_size=page_size)

                for row in results:
                    domain = Domain(row[1], row[2])
                    domain.id = row[0]
                    all_domains.append(domain)
                    
                if page_num > 1:
                    prev_page = page_num - 1
                if len(all_domains) > 0 and (len(all_domains) >= page_size):
                    next_page = page_num + 1
                
                return all_domains, prev_page, next_page
                        
            except oracledb.Error:
                pass

            return all_domains
    
    def get_last_domain_id(self):
        with self.__get_cursor() as cursor:
            result = cursor.execute("SELECT domain_id FROM domains WHERE domain_id = (SELECT MAX(domain_id) FROM domains)")
            for row in result:
                domain_id = int(row[0])
                return domain_id
    
    def get_domain_choices(self):
        domains = self.get_all_domains()
        domain_choices = []

        for domain in domains:
            domain_choices.append((domain.id, domain.name))
        
        return domain_choices
    
    def add_domain(self, domain):
        if domain.id is None:
            with self.__connection.cursor() as cursor:
                cursor.execute("INSERT INTO domains (domain, domain_description) VALUES(:domain, :domain_description)",
                            (domain.name, domain.description))
        elif self.get_domain(domain.id):
            raise ValueError("Domain already exist. Please change the domain id.")

    def modify_domain(self, domain):
        if not self.get_domain(domain.id):
            raise ValueError("Domain does not exist. Please modify an existing domain.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATE domains SET domain=:domain, domain_description=:domain_description WHERE domain_id=:domain_id",
                           (domain.name, domain.description, domain.id))

    def delete_domain(self, domain):
        if not self.get_domain(domain.id):
            raise ValueError("Domain does not exist. Please choose an existing domain to delete.")
        
        with self.__connection.cursor() as cursor:
            cursor.execute("DELETE FROM domains WHERE domain_id=:domain_id", domain_id=domain.id)

    def search_course_id(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses WHERE lower(course_id) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    matches.append(course)

                return matches
            
            except oracledb.Error:
                pass

    def search_course_title(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses WHERE lower(course_title) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    matches.append(course)

                return matches
            
            except oracledb.Error:
                pass

    def search_course_description(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT course_id, course_title, theory_hours, lab_hours,
                work_hours, description, domain_id, term_id FROM courses WHERE lower(description) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    course = Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    matches.append(course)

                return matches
            
            except oracledb.Error:
                pass

    def search_competency_name(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT competency_id, competency, competency_achievement, 
                competency_type FROM competencies WHERE lower(competency) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    matches.append(competency)

                return matches
            
            except oracledb.Error:
                pass

    def search_competency_achievement(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT competency_id, competency, competency_achievement, 
                competency_type FROM competencies WHERE lower(competency_achievement) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    competency = Competency(row[0], row[1], row[2], row[3])
                    matches.append(competency)

                return matches
            
            except oracledb.Error:
                pass

    def search_element_name(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM view_competencies_elements WHERE lower(element) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    matches.append(element)

                return matches
            
            except oracledb.Error:
                pass

    def search_element_criteria(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT element_id, element_order, element, element_criteria, competency_id 
                FROM view_competencies_elements WHERE lower(element_criteria) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    element = Element(row[1], row[2], row[3], row[4])
                    element.id = row[0]
                    matches.append(element)

                return matches
            
            except oracledb.Error:
                pass

    def search_domain_name(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT domain, domain_description, domain_id FROM domains
                WHERE lower(domain) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    domain = Domain(row[0], row[1])
                    domain.id = row[2]
                    matches.append(domain)

                return matches
            
            except oracledb.Error:
                pass

    def search_domain_description(self, search_text):
        with self.__get_cursor() as cursor:
            try:
                matches = []
                search_text = f'\'%{search_text.lower()}%\''
                sql = """SELECT domain, domain_description, domain_id FROM domains
                WHERE lower(domain_description) LIKE """ + search_text

                results = cursor.execute(sql)

                for row in results:
                    domain = Domain(row[0], row[1])
                    domain.id = row[2]
                    matches.append(domain)

                return matches
            
            except oracledb.Error:
                pass
    
    def search_all(self, search_text):
        # I am sorry PDBORA19C
        course_ids = self.search_course_id(search_text)
        course_titles = self.search_course_title(search_text)
        course_descriptions = self.search_course_description(search_text)
        competency_names = self.search_competency_name(search_text)
        comptency_achievements = self.search_competency_achievement(search_text)
        element_names = self.search_element_name(search_text)
        element_criterias = self.search_element_criteria(search_text)
        domain_names = self.search_domain_name(search_text)
        domain_descriptions = self.search_domain_description(search_text)

        course_results = course_ids + course_titles + course_descriptions
        competency_results = competency_names + comptency_achievements
        element_results = element_names + element_criterias
        domain_results = domain_names + domain_descriptions

        return course_results, competency_results, element_results, domain_results

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')