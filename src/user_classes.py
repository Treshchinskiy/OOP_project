
import hashlib


class Account:
    username:str=None
    password:str=None
    email:str=None
    
    def __init__(self, username:str, password:str,email:str):
        self.username = username
        self.password = password
        self.email = email
    
    
    def return_info(self)->list[str]:
        return self.username, self.encrypt_password(self.password), self.email
        
    
    
    @staticmethod
    def encrypt_password(password: str) -> str:
        hash_object = hashlib.sha256()

        hash_object.update(password.encode('utf-8'))
        
        hashed_password = hash_object.hexdigest()

        return hashed_password





class User:
    user_id:int = 1
    is_logged_in:bool = False

    def __init__(self, username:str, password:str,email:str ,preferences=None):
        self.user_id = User.user_id
        User.user_id += 1
        self.preferences:list=preferences
        self.account=Account(username,password,email)
        self.watched_movies:list = []
        self.comments:list = []
        
        
    
    def add_movie_to_watched(self, movie):
        pass
    
    
    def add_comment(self, movie, comment):
        pass
    
    
    def login(self):
        #это какая-то хуйня честно
        pass
        
    
    def logout(self):
        pass
    
    
    