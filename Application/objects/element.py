class Element:
    def __init__(self, order, name, criteria, competency_id):
        if not isinstance(order, int):
            raise TypeError("order must be an int")
        
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(criteria, str):
            raise TypeError("criteria must be a string")
        
        self.order = order
        self.name = name
        self.criteria = criteria
        self.competency_id = competency_id

        self.id = None
        self.hours = None

    def __repr__(self):
        to_return = f'Element(order:{self.order}, name:{self.name}, ' + f'criteria:{self.criteria}, competency_id:{self.competency_id})'
        return to_return
    
    def __str__(self):
        to_return = f'Order: {self.order}, Name: {self.name}, ' + f'Criteria: {self.criteria}, Competency ID: {self.competency_id}'
        return to_return
    
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class ElementForm(FlaskForm):
    order = IntegerField('Element Order', validators=[DataRequired(), NumberRange(min=1)])
    name = StringField('Element', validators=[DataRequired(), Length(min=1, max=250)]) 
    criteria = StringField('Criteria', validators=[DataRequired(), Length(min=1, max=500)])
    competency_id = StringField('Existing Competency', validators=[DataRequired(), Length(min=4, max=4)])