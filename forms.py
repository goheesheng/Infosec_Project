import re
from wtforms import StringField, validators, SubmitField, FileField, PasswordField
from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, BooleanField, FileField, PasswordField, IntegerField
from wtforms_validators import AlphaSpace, AlphaNumeric, Integer

class FileSubmit(Form):
    patient_name = StringField("Patient Name",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submission = FileField("Updated tempalate (Using base template)" )
    submit = SubmitField("Submit")

class RequestPatientInfo_Form(Form):
    patient_id=IntegerField("Patient ID",[validators.DataRequired()])
    submit = SubmitField("Submit")

class Login_form(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Regexp(re.compile('^.+@[^.].*\.[a-z]{2,10}$'), message="Invalid email address.")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')),
    ])
    patient_submit = SubmitField("Submit")
    doctor_submit = SubmitField("Submit")
    researcher_submit = SubmitField("Submit")
    admin_submit = SubmitField("Submit")
    head_admin_submit = SubmitField("Submit")

class Otp(Form):
    otp = StringField("OTP",[validators.Length(min=6, max=6), validators.DataRequired()] )
    submit = SubmitField("Submit")

class Register(Form):
    username = StringField('Username', [validators.DataRequired(),validators.Regexp(re.compile('^([a-zA-Z0-9]+)([a-zA-Z0-9]{2,5})$'),message= "Username can contain only alphanumeric characters!")])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired(),validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")
