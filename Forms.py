from wtforms import Form, StringField, RadioField, SelectField, IntegerField, validators
from wtforms.fields import EmailField

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    position = RadioField('Membership', choices=[('A', 'Assistant'), ('M', 'Manager'), ('O', 'Owner')], default='A')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone = IntegerField('Phone Number',  [validators.DataRequired()])


