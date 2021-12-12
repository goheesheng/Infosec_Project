import re
from wtforms import StringField, validators, SubmitField, FileField, PasswordField
from wtforms import Form, StringField, SelectField, TextAreaField, validators, PasswordField, BooleanField, FileField, PasswordField, IntegerField, DateField
from wtforms_validators import AlphaSpace, AlphaNumeric, Integer
#from wtforms.fields.html5 import DateField #Used for wtforms versions below 3.0.0
#from wtforms.fields.datetime import DateField #Used for wtforms version 3.0.0 onwards

class FileSubmit(Form):
    patient_nric = StringField("Patient NRIC", [validators.DataRequired()])
    patient_name=StringField("Patient Name",[validators.DataRequired()])
    submission = FileField("Updated template (Using base template)" )
    submit = SubmitField("Submit")

class RequestPatientInfo_Form(Form):
    patient_nric=StringField("Patient NRIC",[validators.DataRequired(),validators.Regexp(re.compile('^[STFGstfg]\d{7}[a-zA-Z]$'))])
    submit = SubmitField("Submit")

class Patient_Login_form(Form):
    # username = StringField('NRIC', [validators.DataRequired(), validators.Regexp(re.compile('^[STFGstfd]\d{7}[A-Za-z]$'))])
    username = StringField('NRIC', [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),])
    patient_submit = SubmitField("Submit")

class Admin_Login_form(Form):
    username = StringField('Staff ID', [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')),
    ])
    staff_submit = SubmitField("Submit")

class Otp(Form):
    otp = StringField("OTP",[validators.Length(min=6, max=6), validators.DataRequired()] )
    submit = SubmitField("Submit")

class Register(Form):
    username = StringField('NRIC', [validators.DataRequired(),validators.Regexp(re.compile('^[a-zA-Z]\d{7}[a-zA-Z]$'),message= "Username can contain only alphanumeric characters!")],render_kw={"placeholder": "E.g T1234567T"})
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired(),validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")

class RegisterDoctor(Form):
    username = StringField("Username", [validators.Length(min=1, max=400), validators.DataRequired()])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    department = StringField("Department", [validators.Length(min=1, max=400), validators.DataRequired()])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired(),validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")

class RegisterResearcher(Form):
    username = StringField("Username", [validators.Length(min=1, max=400), validators.DataRequired()])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    company = StringField("Company", [validators.Length(min=1, max=400), validators.DataRequired()])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired(),validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")

class RegisterHr(Form):
    username = StringField("Username", [validators.Length(min=1, max=400), validators.DataRequired()])
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])

    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.DataRequired(),validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")

class Admin_UpdateUserForm(Form):
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', render_kw={"placeholder": "Leave blank to not change password"})
    confirmPassword = PasswordField('Re-enter Password', [validators.EqualTo('password',message='Both password fields must be equal!')])
    roles = SelectField('Change Roles', choices=[('', 'Select'), ('Researcher', 'researchers'), ('Doctor', 'doctors'),('Human Resource', 'hr'),('Patient', 'patient')], default='')

class General_UpdateForm(Form):
    firstname = StringField("First Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    lastname = StringField("Last Name", [validators.Length(min=1, max=400), validators.DataRequired()])
    phone_no = StringField('Phone Number', [validators.Length(min=8, max=15), validators.DataRequired(),Integer()],render_kw={"placeholder": "E.g 8898 2898"})
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(), validators.Regexp('^.+@[^.].*\.[a-z]{2,10}$', message="Invalid email address.")],render_kw={"placeholder": "E.g you@example.com"})
    address = TextAreaField('Address', [validators.DataRequired()],render_kw={"placeholder": "E.g 898 Yishun Ring Road"})
    postal_code = StringField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "889906"})
    password = PasswordField('New Password', [
        validators.Optional() ,validators.Regexp(re.compile('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'), message= "Password must contain 10-20 characters, number, uppercase, lowercase, special character."),
    ])
    confirmPassword = PasswordField('Re-enter Password', [validators.EqualTo('password',message='Both password fields must be equal!')])
    submit = SubmitField("Submit")
  

class Appointment(Form):
    date = DateField("Enter date for appointment", validators=[validators.DataRequired()])
    time = SelectField("Choose time", choices=[("10 A.M."),("11 A.M."),("12 P.M."),("1 P.M."),("2 P.M."),("3 P.M."),("4 P.M."),("5 P.M.")],validators=[validators.DataRequired()])
