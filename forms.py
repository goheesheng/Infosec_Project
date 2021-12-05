from flask_wtf import FlaskForm
import re
from wtforms import StringField, validators, SubmitField, FileField, PasswordField

class FileSubmit(FlaskForm):
    sender = StringField("Sender",[validators.Length(min=1, max=400), validators.DataRequired()] )
    recipient = StringField("Recipient",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submission = FileField("Submission" )
    submit = SubmitField("Submit")

class Login_form(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Regexp(re.compile('^.+@[^.].*\.[a-z]{2,10}$'), message="Invalid email address.")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')),
    ])
    submit = SubmitField("Submit")

class Otp(FlaskForm):
    otp = StringField("OTP",[validators.Length(min=6, max=6), validators.DataRequired()] )
    submit = SubmitField("Submit")

class Register(FlaskForm):
    username = StringField('Username', [validators.DataRequired(),validators.Regexp(re.compile('^([a-zA-Z0-9]+)([a-zA-Z0-9]{2,5})$'),message= "Username can contain only alphanumeric characters!")])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), validators.Regexp(re.compile('^.+@[^.].*\.[a-z]{2,10}$'), message="Invalid email address.")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
        validators.EqualTo('confirmPassword', message='Passwords do not match.')
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired()])
    submit = SubmitField("Submit")