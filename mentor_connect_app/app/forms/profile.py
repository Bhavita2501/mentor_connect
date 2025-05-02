from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    location = SelectField('Location', choices=[
        ('', 'Select Location'),
        ('new_york', 'New York'),
        ('san_francisco', 'San Francisco'),
        ('london', 'London'),
        ('tokyo', 'Tokyo'),
        ('remote', 'Remote')
    ], validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')

class MentorProfileForm(FlaskForm):
    title = StringField('Professional Title', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company/Organization', validators=[Optional(), Length(max=100)])
    experience_years = IntegerField('Years of Experience', validators=[DataRequired(), NumberRange(min=0, max=50)])
    hourly_rate = FloatField('Rate ($ per 30 minutes)', validators=[DataRequired(), NumberRange(min=20, message="Minimum rate is $20 per 30 minutes")])
    location = SelectField('Location', choices=[
        ('', 'Select Location'),
        ('new_york', 'New York'),
        ('san_francisco', 'San Francisco'),
        ('london', 'London'),
        ('tokyo', 'Tokyo'),
        ('remote', 'Remote')
    ], validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired(), Length(max=500)], 
                         description='Enter your skills separated by commas (e.g., Python, JavaScript, Project Management)')
    bio = TextAreaField('Professional Bio', validators=[DataRequired(), Length(max=1000)])
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Mentor Profile')