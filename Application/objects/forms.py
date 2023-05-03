from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=10, max=100)])
    name = StringField('Username', validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    avatar = FileField('Avatar', validators=[FileAllowed(['png'])])
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=10, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me?')
    
class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    retype_new_password = PasswordField('Retype New Password', validators=[DataRequired(), Length(min=8)])

class CompetencyForm(FlaskForm):
    id = StringField('Competency ID', validators=[DataRequired(), Length(min=4, max=4)])
    name = StringField('Competency Name', validators=[DataRequired(), Length(min=10, max=250)])
    achievement = TextAreaField('Achievement', validators=[DataRequired(), Length(min=10, max=500)])
    type = SelectField('Choose an type', choices=[('Mandatory'), ('Complementary')], validators=[DataRequired()])

class CourseForm(FlaskForm):
    id = StringField('Course ID', validators=[DataRequired(), Length(min=10, max=100)])
    title = StringField('Course Title', validators=[DataRequired(), Length(min=10, max=100)])
    theory_hours = IntegerField('Theory Hours', validators=[DataRequired(), NumberRange(min=0, max=3)])
    lab_hours = IntegerField('Lab Hours', validators=[DataRequired(), NumberRange(min=0, max=3)])
    work_hours = IntegerField('Work Hours', validators=[DataRequired(), NumberRange(min=0, max=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    domain_id = SelectField('Existing Domain', validators=[DataRequired()])
    term_id = SelectField('Choose a term', choices=[('1', '1 Fall'), ('2', '2 Winter'), ('3', '3 Fall'), ('4', '4 Winter'), ('5', '5 Fall'), ('6', '6 Winter')])

class DomainForm(FlaskForm):
    name = StringField('Domain Name', validators=[DataRequired(), Length(min=1, max=50)]) 
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=500)])

class ElementForm(FlaskForm):
    order = IntegerField('Element Order', validators=[DataRequired(), NumberRange(min=1)])
    name = StringField('Element', validators=[DataRequired(), Length(min=1, max=250)]) 
    criteria = TextAreaField('Criteria', validators=[DataRequired(), Length(min=1, max=500)])
    competency_id = StringField('Existing Competency', validators=[DataRequired(), Length(min=4, max=4)])

class CourseElementForm(FlaskForm):
    hours = IntegerField('Number Of Hours This Element Will Be Worked On', validators=[DataRequired(), NumberRange(min=1)])
    # The choices are set after the form is created
    id = SelectField('Element', validators=[DataRequired()])

# find way to use 1 class
class DeleteMemberForm(FlaskForm):
    users = SelectField('Select a Member to Delete')
class DeleteUserAdminForm(FlaskForm):
    users = SelectField('Select a User Admin to Delete')
class DeleteAdminForm(FlaskForm):
    users = SelectField('Select an Admin to Delete')

# find way to use 1 class
class BlockMemberForm(FlaskForm):
    unblocked_members = SelectField('Select a Member to Block')
class UnblockMemberForm(FlaskForm):
    blocked_members = SelectField('Select a Member to Unblock')

# find way to use 1 class
class MoveMemberForm(FlaskForm):
    users = SelectField("Select a Member to Move")
    groups = SelectField("to")
class MoveUserAdminForm(FlaskForm):
    users = SelectField('Select a User Admin to Move')
    groups = SelectField('to')
class MoveAdminForm(FlaskForm):
    users = SelectField('Select an Admin to Move')
    groups = SelectField('to')

class SearchForm(FlaskForm):
    query = StringField(validators=[DataRequired()], render_kw={"placeholder": "Enter Search Query"})