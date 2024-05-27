from src import db_classes
from src import user_classes
from flask import Flask,render_template, request,redirect

#keyBERT
#Huggingface - модели глянуть 
#rake_nltk


'''
как во flask приложении сделать так чтобы пользователь который зашел в систему 
сохранился и чтобы мы дальше могли обращаться к нему в функциях
'''

Users_db = db_classes.UserDatabase('localhost','root','1474747vd','oop_project_userinfo')



app=Flask(__name__)
app.secret_key = 'ILIFIA80'



@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def login():
    return render_template('login.html')



@app.route('/registration')
def register():
    return render_template('registration.html')



@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['uemail']
        password = request.form['upassword']
        if Users_db.check_exist_user(name,email):
            error = 'User with name ' + name + ' already exists or try to change email address'
            return render_template('registration.html', error=error)
        
        
        try: 
            if not db_classes.UserDatabase.is_strong_password(password):
                error = "Change password"
                return render_template('registration.html', error=error)
            password=user_classes.Account.encrypt_password(password)
            Users_db.insert_user(name,password, email )
        except Exception as e:
            err='Error occurred while inserting user'
            return render_template('error.html',error_message=err)
    return redirect('/home')



@app.route('/login_validation',methods=['POST'])
def login_validate():
    if request.method=='POST':
        password=user_classes.Account.encrypt_password(request.form['password'])
        email=request.form['email']
        if Users_db.check_login_validation(password,email):
            return redirect('/home')
        else:
            error = "User not found"
            return render_template('login.html',error=error)
    




if __name__ == '__main__':
    app.run(debug=True)
    
    
