from wtforms import Form, StringField, SelectField, IntegerField,DateField, TimeField, validators
from wtforms.fields import EmailField

class CheckoutForm(Form):
    collection = SelectField('Collection Method', [validators.DataRequired()], choices=[('', 'Select'), ('S', 'Self Pick-up'), ('D', 'Delivery')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone = IntegerField('Phone Number', [validators.DataRequired(), validators.length(8)])
    billing_address = StringField('Billing Address', [validators.DataRequired])
    date_slot = DateField('Date', [validators.DataRequired()])
    time_slot = TimeField('Time', [validators.DataRequired])
    payment = SelectField('Payment Method', [validators.DataRequired()])