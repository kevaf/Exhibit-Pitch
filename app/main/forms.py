from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class Form(FlaskForm):
    text = TextAreaField('Give your Review:',validators=[Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    text = TextAreaField('Text',validators=[Required()])
    category = SelectField('Type',choices=[('investor','Pitch for Investors'),('employee','Pitch for Employees'),('customer','Pitch for Employees')],validators=[Required()])
    submit = SubmitField('Submit')