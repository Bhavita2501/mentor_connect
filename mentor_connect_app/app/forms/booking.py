from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField, HiddenField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime, time

class BookingForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = SelectField('Time', validators=[DataRequired()])
    notes = TextAreaField('Message to mentor', validators=[Optional(), Length(max=500)])
    mentor_id = HiddenField('Mentor ID', validators=[DataRequired()])
    submit = SubmitField('Book Session')
    
    def validate_date(self, date):
        if date.data < datetime.now().date():
            raise ValueError("Cannot book sessions in the past")

class SessionFeedbackForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    comment = TextAreaField('Your feedback', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit Feedback')