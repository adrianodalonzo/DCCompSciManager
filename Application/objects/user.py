from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name, password):
        if not isinstance(email, str):
            raise TypeError("email must be a string")

        if name.isalnum() == False:
            raise TypeError("name must only contain alphanumeric characters")

        if not isinstance(password, str):
            raise TypeError("password must be a string")
        
        self.email = email
        self.name = name
        self.password = password

        self.id = None
        self.group = None
    
    def __repr__(self):
        return f'User: ({self.email}, {self.name}, {self.password}, {self.id}, {self.group})'
    
    def __str__(self):
        return f'Email: {self.email}, Name: {self.name}, Password: {self.password}, ID: {self.id}, Group: {self.group}'


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=10, max=100)])
    name = StringField('Username', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    avatar = FileField('Avatar', validators=[FileAllowed(['png'])])
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=10, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me?')
    
#TODO: Add form here for resetting a password
class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    retype_new_password = PasswordField('Retype New Password', validators=[DataRequired(), Length(min=8)])