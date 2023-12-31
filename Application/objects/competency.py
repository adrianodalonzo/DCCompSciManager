class Competency:
    def __init__(self, id, name, achievement, type):
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(achievement, str):
            raise TypeError("achievement must be a string")
        
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        
        self.id = id
        self.name = name
        self.achievement = achievement
        self.type = type
        
    def __repr__(self):
        return f'Competency(id:{self.id}, name:{self.name}, achievement:{self.achievement}, type:{self.type})'
    
    def __str__(self):
        to_return = f'Id:{self.id}, Name: {self.name}, Achievement: {self.achievement}, Type: {self.type}'
        return to_return
        
    def from_json(competency_dict):
        if not isinstance(competency_dict, dict):
            raise TypeError("Excepted dict")
        return Competency(competency_dict['id'], competency_dict['name'], competency_dict['achievement'], competency_dict['type'])
    
    def to_json(self, current_url, urls):
        return {'id': self.id, 'name': self.name, 'achievement': self.achievement, 'type': self.type, 'url':current_url, 'element_urls': urls}
        
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

class CompetencyForm(FlaskForm):
    id = StringField('Competency ID', validators=[DataRequired(), Length(min=4, max=4)])
    name = StringField('Competency Name', validators=[DataRequired(), Length(min=10, max=100)])
    achievement = StringField('Achievement', validators=[DataRequired(), Length(min=10, max=100)])
    type = SelectField('Choose an type', choices=[('Mandatory'), ('Complementary')])