# form.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    name = StringField('Name of the Puppy')
    submit = SubmitField('Add Puppy')

class DelForm(FlaskForm):
    id = IntegerField('ID of the puppy')
    submit = SubmitField('Remove Puppy')

class AddOwnerForm(FlaskForm):
    name = StringField('Owner name')
    puppy_id = IntegerField('Puppy ID')
    submit = SubmitField('Add Owner')