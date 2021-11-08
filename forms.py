from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, FileField

class File_submit(FlaskForm):
    sender = StringField("Sender",[validators.Length(min=1, max=400), validators.DataRequired()] )
    recipient = StringField("Recipient",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submission = FileField("hello")
    submit = SubmitField("Submit")