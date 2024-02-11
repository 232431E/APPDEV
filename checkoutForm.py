from wtforms import Form, StringField, SelectField, DateField, validators, TimeField
from wtforms.fields import EmailField

class CheckoutForm(Form):
    collection = SelectField('Collection Method', [validators.DataRequired()], choices=[('', 'Select'), ('Self Pick-up', 'Self Pick-up'), ('Delivery', 'Delivery')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.DataRequired(), validators.length(8)])
    address = StringField('Address', [validators.DataRequired()])
    date_slot = DateField('Date', [validators.DataRequired()])
    time_slot = TimeField('Time', [validators.DataRequired()])
    payment = SelectField('Payment Method', [validators.DataRequired()],
                      choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('Cash-On-Delivery', 'Cash-On-Delivery'), ('Paynow', 'Paynow')],
                      default='')


