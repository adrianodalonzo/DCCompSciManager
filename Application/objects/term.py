class Term:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        self.name = name
        self.id = None

    def __repr__(self):
        return f'Term(id:{self.id}, name:{self.name})'
    
    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}'

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class TermForm(FlaskForm):
    name = StringField('Term Name', validators=[DataRequired(), Length(min=1, max=6)])