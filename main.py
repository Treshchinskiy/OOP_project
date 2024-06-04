from flask import Flask, render_template, redirect, flash, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from src.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, User
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd


df=pd.read_csv('datasets/complete.csv')


#keyBERT
#Huggingface 
#rake_nltk




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




@app.route('/search',methods=['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        query = request.args.get('q')



    return render_template('search.html')










tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


@app.route('/chat/')
def index2():
    return render_template('chat.html')



@app.route('/get', methods=['GET','POST'])
def chat():
    msg=request.form["msg"]
    input = msg
    return get_chat_response(input)



def get_chat_response(text):
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)



from transformers import BertTokenizer, BertForSequenceClassification
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
#нахуй не надо



from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


vectorizer = TfidfVectorizer(stop_words='english')


overview_vectors = vectorizer.fit_transform(df['overview'].values.astype('U'))


@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        user_description = request.form['description']
        
        # Вычисление TF-IDF вектора для описания пользователя
        user_vector = vectorizer.transform([user_description])
        
        # Вычисление косинусного расстояния между вектором пользователя и векторами фильмов
        similarities = cosine_similarity(user_vector, overview_vectors)
        
        # Получение индексов наиболее похожих фильмов
        similar_indices = similarities.argsort()[0][::-1][:5]
        
        # Формирование списка наиболее похожих фильмов с описанием
        similar_movies = []
        for idx in similar_indices:
            movie = df.iloc[idx]
            similar_movies.append({
                'title': movie['title'],
                'overview': movie['overview'],
            })
        
        return render_template('find.html', movies=similar_movies)
    
    
    return render_template('find.html')







'''
у меня такая задача: пользователь пишет текст пожелания того какой 
бы он фильм хотел бы посмотреть например "хочу посмотреть боевик с 
джони дэпом в главной роли" и мне нужна модель которая будет выделять 
ключевые слова этого предложения а потом сравнивать со столбцом в датафрейме 
о фильмах и находить наиболее похожий под описание фильм как это сделат
'''


import spacy


#nlp = spacy.load("en_core_web_sm")
#nlp.to_disk("spacy_model")

nlp = spacy.load("spacy_model")

# Функция для извлечения ключевых слов из различных столбцов фильма
def extract_keywords(row):
    text = ' '.join(str(cell) for cell in row if isinstance(cell, str))
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(keywords)



import joblib

#df['combined_text'] = df[['genres', 'keywords', 'overview', 'cast', 'crew']].apply(extract_keywords, axis=1)

df = joblib.load('df_combined_text.joblib')


vectorizer2 = joblib.load('vectorizer2.joblib')

# Загрузка TF-IDF векторов описаний фильмов
overview_vectors2 = joblib.load('overview_vectors2.joblib')

import numpy as np


def find_similar_movie(user_query):
    # Преобразование запроса пользователя в TF-IDF вектор
    user_vector = vectorizer2.transform([extract_keywords([user_query])])
    
    # Вычисление косинусного сходства между запросом пользователя и описаниями фильмов
    similarities = cosine_similarity(user_vector, overview_vectors2)
    
    # Получение индекса наиболее похожего фильма
    similar_index = np.argmax(similarities)  # Используем np.argmax() вместо similarities.argmax()
    
    # Получение информации о наиболее похожем фильме
    similar_movie = df.iloc[similar_index]
    
    return similar_movie



@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        user_query = request.form['user_query']
        recommended_movie = find_similar_movie(user_query)
        recommended_movie_title=recommended_movie['title']
        recommended_movie_overview=recommended_movie['overview']
        return render_template('recommend.html', user_query=user_query,recommended_movie_title=recommended_movie_title,
                               recommended_movie_overview=recommended_movie_overview)
    return render_template('recommend.html')








    
    
  
if __name__ == '__main__':
    app.run(debug=True)
    
    
