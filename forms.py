from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class SearchForm(Form):
	search = StringField(" ", [validators.Length(min=4, max=30)], render_kw={'placeholder':'Search'})

class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=2, max=20)], render_kw={'placeholder'':Name'})
    email = EmailField("Email", [validators.Length(min=6, max=20)], render_kw={'placeholder':'Email'})
    username = StringField(" ", [validators.Length(min=5, max=10)], render_kw={'placeholder':'Username'})
    password = PasswordField("Password", [validators.Length(min=5)], render_kw={'placeholder':'Password'})
    confirmPw = PasswordField("Confirm Password", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])