import shelve

from wtforms import Form, StringField, SelectField, TextAreaField, validators, ValidationError
from wtforms.fields import EmailField, DateField


class LoginForm(Form):
    user_id = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=30), validators.DataRequired()])


class RegistrationForm(Form):
    user_id = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.Length(max=200), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=30), validators.DataRequired()])

    # def validate_user_id(form, field):
    #     customers_dict = {}
    #     db = shelve.open('customer.db', 'c')
    #
    #     try:
    #         customers_dict = db['Customers']
    #     except KeyError:
    #         print('Error in retrieving Customers from customer.db')
    #     db.close()
    #
    #     if field.data in customers_dict:
    #         raise ValidationError('Username already exists.')
