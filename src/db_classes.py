
import mysql.connector
import re



class UserDatabase:
    host:str=None
    user:str=None
    password:str=None
    database:str=None
    connection=None
    
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_database()

    
    def connect_to_database(self)-> mysql.connector.connection.MySQLConnection:
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            return None
        
        
    def close_connection(self)->mysql.connector.connection.MySQLConnection:
        self.connection.close()
        return self.connection
    
    
    def insert_user(self,name,password,email):
        cursor=self.connection.cursor()
        query="INSERT INTO users (name, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name,password,email))
        self.connection.commit()
        cursor.close()
        
        
        
    def update_username(self,name,new_password):
        cursor=self.connection.cursor()
        cursor.closer()
        
        
    

    def  delete_user(self, username:str):
        cursor=self.connection.cursor()
        cursor.closer()

        
    
    def get_user_by_name(self, username: str) -> list:
        try:
            cursor = self.connection.cursor()
            
            cursor.callproc('get_user_by_username', [username])
            
            for result in cursor.stored_results():
                rows = result.fetchall()
                
            cursor.close()
            return rows
        except mysql.connector.Error as e:
            print("Error occurred:", e)
            return None
        
    def check_exist_user(self, username: str,email:str) -> bool:
        try:
            cursor = self.connection.cursor()
            
            cursor.callproc('check_exist_user',[username,email])
            
            for result in cursor.stored_results():
                rows = result.fetchall()
                
                
            cursor.close()
            
            return bool(rows[0][0]) 
        
        except Exception as e:
            print(e)
            print("Error occurred")
            return None

    def check_login_validation(self,password:str,email:str)->bool:
        try:
            cursor=self.connection.cursor()
            
            cursor.callproc('check_login_validation',[password, email])
            
            for result in cursor.stored_results():
                rows=result.fetchall()
            print(rows)
            
            
            return bool(rows[0][0])
        
        except Exception as e:
            print(e)
            print("Error occurred")
            return None
        
        
    @staticmethod
    def is_strong_password(password):
        if len(password) < 8:
            return False
        
        has_lower = re.search(r'[a-z]', password)
        has_upper = re.search(r'[A-Z]', password)
        
        
        if has_lower and has_upper:
            return True
        else:
            return False



if __name__ == '__main__':
    a=UserDatabase('localhost','root','1474747vd','oop_project_userinfo')
    print(a.check_exist_user('flo1','vlad.treshchindkiy.03@mail.ru'))
    print(a.check_exist_user('vlad1','q'))

    





