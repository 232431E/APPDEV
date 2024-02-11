from flask import Flask, render_template, request, redirect, url_for
from checkoutForm import CheckoutForm
from customerLoginRegistrationForm import LoginForm, RegistrationForm
import shelve, Checkout, customerMutatorandAccessor

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('customerHome.html')

@app.route('/customerCheckout', methods=['GET', 'POST'])
def checkout():
    checkout = CheckoutForm(request.form)
    order_dict = {}
    db = shelve.open('sale.db', 'c')
    if request.method == 'POST' and checkout.validate():
        try:
            order_dict = db['Orders']
        except:
            print('Error in retrieving Orders from sale.db')

        order = Checkout.Checkout(checkout.collection.data, checkout.email.data, checkout.phone.data, checkout.address.data,
                        checkout.date_slot.data, checkout.time_slot.data, checkout.payment.data)
        db['Orders'] = order_dict
        order_dict[order.get_order_id()] = order
        db.close()

        return redirect(url_for('confirmation'))
    return render_template('/customerCheckout.html', form=checkout)

@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    with shelve.open('sale.db') as db:
        order_dict = db.get('Orders', {})
        checkout = order_dict.get(order_id)
    return render_template('confirmation.html', checkout=checkout)
@app.route('/customerLogin', methods=['GET', 'POST'])
def login():
    # login
    create_login_form = LoginForm(request.form)
    if request.method == 'POST' and create_login_form.validate():

        try:
            db = shelve.open('customer.db', 'r')
            customer_dict = db['Customers']
            db.close()
            user_id = create_login_form.user_id.data
            cust = customer_dict[user_id]
            correct_pwd = cust.get_password()
            password = create_login_form.password.data

            if password == correct_pwd:
                print('Success')
                return render_template('customerCheckout.html')

            else:
                print('Invalid password or username. Please try again.')
                return render_template('customerLogin.html')

        except:
            print("Error in retrieving Customers from customer.db in login.")
            db.close()
            return render_template('customerLogin.html', form=create_login_form)

    return render_template('customerLogin.html', form=create_login_form)


@app.route('/customerRegistration', methods=['GET', 'POST'])
def registration_customer():
    # registration
    create_registration_form = RegistrationForm(request.form)
    if request.method == 'POST' and create_registration_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']

        except:
            print("Error in retrieving Customers from customer.db from register.")

        # hashed_password = Customer.Registration.hash_password(create_registration_form.password.data)
        user_id = create_registration_form.user_id.data

        if user_id in customers_dict:
            db.close()
            return render_template('customerRegistration.html', form=create_registration_form)

        customer = customerMutatorandAccessor.Registration(create_registration_form.first_name.data,
                                                           create_registration_form.last_name.data,
                                                           create_registration_form.gender.data,
                                                           create_registration_form.email.data,
                                                           create_registration_form.date_joined.data,
                                                           create_registration_form.address.data,
                                                           create_registration_form.user_id.data,
                                                           create_registration_form.password.data)
        # customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict

        db.close()
        print('Account created successfully!')

        return redirect(url_for('retrieve_customers'))
    return render_template('customerRegistration.html', form=create_registration_form)


@app.route('/retrieveCustomers')
def retrieve_customer_details():
    # check customer personal information
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('retrieveCustomerDetails.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateCustomer/<id>', methods=['GET', 'POST'])
def update_customer(id):
    # update personal information in settings?
    update_customer_form = RegistrationForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customer_details'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.password.data = customer.get_password()

        return render_template('updateCustomerDetails.html', form=update_customer_form)


@app.route('/deleteCustomer/<id>', methods=['POST'])
def delete_customer(id):
    # delete customer information
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return render_template('customerHome.html')

if __name__ == '__main__':
    app.run(debug=True)