from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, FileField

class FileSubmit(FlaskForm):
    sender = StringField("Sender",[validators.Length(min=1, max=400), validators.DataRequired()] )
    recipient = StringField("Recipient",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submission = FileField("Submission" )
    submit = SubmitField("Submit")

class Login_form(FlaskForm):
    email = StringField("Email",[validators.Length(min=1, max=400), validators.DataRequired()] )
    password = StringField("Password",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submit = SubmitField("Submit")

class Otp(FlaskForm):
    otp = StringField("OTP",[validators.Length(min=6, max=6), validators.DataRequired()] )
    submit = SubmitField("Submit")

class Register(FlaskForm):
    username = StringField("Username", [validators.Length(min=1, max=400), validators.DataRequired()])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    email = StringField("Email", [validators.Length(min=1, max=400), validators.DataRequired()])
    password = StringField("Password", [validators.Length(min=1, max=400), validators.DataRequired()])
    submit = SubmitField("Submit")