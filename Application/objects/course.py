class Course:
    def __init__(self, id, title, theory_hours, lab_hours, work_hours, description, domain_id, term_id):
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        
        if not isinstance(theory_hours, int):
            raise TypeError("theory_hours must be an int")
        
        if not isinstance(lab_hours, int):
            raise TypeError("lab_hours must be an int")
        
        if not isinstance(work_hours, int):
            raise TypeError("work_hours must be an int")
        
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        
        if not isinstance(domain_id, int):
            raise TypeError("domain_id must be an int")
        
        if not isinstance(term_id, int):
            raise TypeError("term_id must be an int")
        
        self.id = id
        self.title = title
        self.theory_hours = theory_hours
        self.lab_hours = lab_hours
        self.work_hours = work_hours
        self.description = description
        self.domain_id = domain_id
        self.term_id = term_id
    
    def __repr__(self):
        to_return = f'Course(id:{self.id}, title:{self.title}, theory_hours:{self.theory_hours}, ' + f'lab_hours:{self.lab_hours}, work_hours:{self.work_hours}, ' + f'description:{self.description}, domain_id:{self.domain_id}, ' + f'term_id:{self.term_id}, id:{self.id})'
        return to_return
    
    def __str__(self):
        to_return = f'Id:{self.id}, Title: {self.title}, Theory Hours: {self.theory_hours}, ' + f'Lab Hours: {self.lab_hours}, Work Hours: {self.work_hours}, ' + f'Description: {self.description}, Domain ID: {self.domain_id}, ' + f'Term ID: {self.term_id}'
        return to_return
    
    def from_json(course_dict):
        if not isinstance(course_dict, dict):
            raise TypeError("Excepted dict")
        return Course(course_dict['id'], course_dict['title'], course_dict['theory_hours'], course_dict['lab_hours'], course_dict['work_hours'], course_dict['description'], course_dict['domain_id'], course_dict['term_id'])
        
    def to_json(self):
        return {'id': self.id, 'title': self.title, 'theory_hours': self.theory_hours, 'lab_hours': self.lab_hours, 'work_hours': self.work_hours, 'description': self.description, 'domain_id': self.domain_id, 'term_id': self.term_id}
    
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length

class CourseForm(FlaskForm):
    id = StringField('Course ID', validators=[DataRequired(), Length(min=10, max=100)])
    title = StringField('Course Title', validators=[DataRequired(), Length(min=10, max=100)])
    theory_hours = IntegerField('Theory Hours', validators=[DataRequired(), Length(min=1, max=3)])
    lab_hours = IntegerField('Lab Hours', validators=[DataRequired(), Length(min=1, max=3)])
    work_hours = IntegerField('Work Hours', validators=[DataRequired(), Length(min=1, max=3)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    domain = StringField('Existing Domain', validators=[DataRequired(), Length(min=1, max=50)])
    term = SelectField('Choose an term', choices=[('1', 'Fall'), ('2', 'Winter')])