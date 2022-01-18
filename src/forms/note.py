from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=128)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=10)])


class CreationNoteForm(NoteForm):
    submit = SubmitField('Create note')


class UpdatedNoteForm(NoteForm):
    submit = SubmitField('Update note')
