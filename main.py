from flask import Flask, render_template, redirect, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from src.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, User


'''мне нужно написать веб сайт на flask для персоналлизированной реккомендации фильмов пользователю. 
Логика программы: для начала у нас базовый список предложений фильмов  в зависимости от выбора фильма 
пользователем. Затем пользователь может оставить комментарии к реккомендации например  "мне не очень 
понравился фильм так как фильм слишком долгий и режисер такой себе" и у нас будет модель которая будет 
анализировать эти комментарии и например из этого вычленять что пользователю не понравилась длина фильма 
и режисер и будет меньше реккомендовать фильмов с этим режиссером и фильмы меньшие по длительности. Помоги 
придумать структуру классов для этого проекта'''


#keyBERT
#Huggingface 
#rake_nltk

# посмотреть как юзать api gpt





bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



with app.app_context():
    db.create_all()





@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

    





@app.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()  
    
    if request.method=='POST':
        if form.validate_on_submit():
            username = form.username.data
            email=form.email.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/') 
        else:
            print('Form validation failed')
            print(form.errors) 

        
    return render_template('registration.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

  
if __name__ == '__main__':
    app.run(debug=True)
    
    
