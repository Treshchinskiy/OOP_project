
import mysql.connector


'''
CREATE DEFINER=`root`@`localhost` PROCEDURE `select_all`()
BEGIN

   SELECT * FROM users;

END

вот создание простой stored proccedure

и потом в коде написать call select_all - и тогда она вызовется

drop procedure select_all - чтобы удалить


CREATE DEFINER=`root`@`localhost` PROCEDURE `find_by_name`(IN name_find varchar(200))
BEGIN
	select * 
    from users
    Where name = name_find;

END

вот эта с параметром нужно задать IN имя любое и тип переменной
и затем при вызове
call find_by_name('vlad') - например
'''


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
        
        
    

    def  delete_user(self, username):
        cursor=self.connection.cursor()
        cursor.closer()

        
    
    def get_user_by_name(self, username)->list[str]:
        try:
            cursor = self.connection.cursor()
            query = "CALL get_user_by_username('{}')".format(username)  # Добавляем кавычки вокруг username
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            if result == []:
                print('User not found')                
                return None
            return result
        except Exception as e:
            print(e)
            print("Error occurred")
            return None
        



a=UserDatabase('localhost','root','1474747vd','oop_project_userinfo')
print(a.get_user_by_name('vlad1'))




