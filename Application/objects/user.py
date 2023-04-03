from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name, password, avatarlink):
        if not isinstance(email, str):
            raise TypeError("email must be a string")

        if name.isalnum() == False:
            raise TypeError("name must only contain alphanumeric characters")

        if not isinstance(password, str):
            raise TypeError("password must be a string")

        if not isinstance(avatarlink, str):
            raise TypeError("avatarlink must be a string")
        
        self.email = email
        self.name = name
        self.password = password
        self.avatarlink = avatarlink

        self.id = None
        self.group = None
    
    def __repr__(self):
        return f'User: ({self.email}, {self.name}, {self.password}, {self.avatarlink}, {self.id}, {self.group})'
    
    def __str__(self):
        return f'Email: {self.email}, Name: {self.name}, Password: {self.password}, AvatarLink: {self.avatarlink}, ID: {self.id}, Group: {self.group}'


from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class SignUpForm(FlaskForm):
    email = EmailField(DataRequired(), Length(min=3, max=100))
    name = StringField(DataRequired(), Length(min=1, max=100))
    password = PasswordField(DataRequired(), Length(min=1))
    avatarlink = StringField()
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1)])
    remember_me = BooleanField('Remember Me?')