from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError



class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
   
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        from app import User
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

    def validate_email(self, email):
        from app import User
        existing_email = User.query.filter_by(
            email=email.data).first()
        if existing_email:
            raise ValidationError(
                'That email already exists. Please choose a different one.')
            

    
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    


