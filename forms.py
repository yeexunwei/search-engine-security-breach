from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    username = StringField('Term', validators=[DataRequired(), Length(min=2, max =50)])
    submit = SubmitField('Search')



from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, HiddenField

from wtforms import validators, ValidationError

class Form1(Form):
    name = StringField('name')
    number = HiddenField('number')
    term = HiddenField('term')
    rate = RadioField('rate', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit1 = SubmitField('submit')

class Form2(Form):
    name = StringField('name')
    submit2 = SubmitField('submit')