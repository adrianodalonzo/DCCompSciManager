class Domain:
    def __init__(self, name, description):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        
        self.name = name
        self.description = description

        self.id = None
    
    def __repr__(self):
        return f'Domain(id:{self.id}, name:{self.name}, description:{self.description})'
    
    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Description: {self.description}'
    
    def from_json(domain_dict):
        if not isinstance(domain_dict, dict):
            raise TypeError("Excepted dict")
        return Domain(domain_dict['name'], domain_dict['description'])
    
    def to_json(self):
        return {'name': self.name, 'description': self.description}
    
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CompetencyForm(FlaskForm):
    name = StringField('Domain Name', validators=[DataRequired(), Length(min=1, max=25)]) 
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=50)])
    
