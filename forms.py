from wtforms import Form, BooleanField, StringField, validators, FileField, TextAreaField

class File_submit(Form):
    document = FileField("Document Submission", [validators.regexp('^[^/\\]\.jpg$')])
    description = TextAreaField("Document Submission")