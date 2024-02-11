from wtforms import Form, StringField, validators, PasswordField, EmailField

class requestMeatForm(Form):
    meat = StringField('Meat', [validators.Length(min=1, max=150), validators.DataRequired()])
    weight = StringField('Weight', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])

class signupForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class loginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class updateProfileForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    