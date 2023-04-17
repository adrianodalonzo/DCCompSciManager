import oracledb
import os
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
            cursor.execute("""insert into courses_users (username, email, password, user_group, blocked) 
                           values (:username, :email, :password, 'Member', '0')""",
                           username=user.name, 
                           email=user.email, 
                           password=user.password)
    
    def fetch_blocked(self, result):
        if result == '1':
            return True
        return False
            
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
                user.blocked = self.fetch_blocked(result[5])
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
                user.blocked = self.fetch_blocked(result[5])
                return user
            
    def update_user_password(self, email, password):
        if not isinstance(password, str):
            raise TypeError('Password MUST be a string!')
        
        if not isinstance(email, str):
            raise TypeError('Email MUST be a string!')
        
        with self.__get_cursor() as cursor:
            user_id = self.get_user(email).id
            cursor.execute('update courses_users set password = :password where user_id = :id', password=password, id=user_id)

    def get_members(self):
        members = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Member'")
            for result in results:
                member = User(result[0], result[3], result[1])
                member.id = result[2]
                member.group = result[4]
                member.blocked = self.fetch_blocked(result[5])
                members.append(member)
        return members
    
    def get_unblocked_members(self):
        members = []
        with self.__get_cursor() as cursor:
            results = cursor.execute("select email, password, user_id, username, user_group, blocked from courses_users where user_group = 'Member' and blocked = '0'")
            for result in results:
                member = User(result[0], result[3], result[1])
                member.id = result[2]
                member.group = result[4]
                member.blocked = self.fetch_blocked(result[5])
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
                member.blocked = self.fetch_blocked(result[5])
                members.append(member)
        return members
    
    def delete_member(self, email):
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

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')