from flask import Flask, render_template, request, redirect, url_for
from Login_Register_Form import LoginForm, RegistrationForm
import shelve
import Customer_login_register
import requests

# For making API requests to Snatchbot

app = Flask(__name__)


def get_db():
    return shelve.open('customer.db', 'c')


@app.route('/')
def home():
    return render_template('home.html')


# def loginCustomer(username, password):
#     with get_db() as db:
#         for user_id, user in db.items():
#             if user.username == username and check_password_hash(user.password, password):
#                 session['user_id'] = user.user_id
#                 flash('Login successful!', 'success')
#                 return redirect(url_for('profile'))
#         flash('Invalid username or password.', 'error')
#         return redirect(url_for('login'))


@app.route('/Login', methods=['GET', 'POST'])
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
                return render_template('logined.html')

            else:
                print('Invalid password or username. Please try again.')
                return render_template('Login.html')

        except:
            print("Error in retrieving Customers from customer.db in login.")
            db.close()
            return render_template('Login.html', form=create_login_form)

    return render_template('Login.html', form=create_login_form)


@app.route('/Registration', methods=['GET', 'POST'])
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
            return render_template('Registration.html', form=create_registration_form)

        customer = Customer_login_register.Registration(create_registration_form.first_name.data,
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

        return redirect(url_for('login'))
    return render_template('Registration.html', form=create_registration_form)


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
    return render_template('retrieveDetails.html', count=len(customers_list), customers_list=customers_list)


# got something wrong in the update function that doesn't update details into the database #
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

        print('Customer details successfully updated')
        return redirect(url_for('retrieve_customer_details'))

    else:
        try:
            customers_dict = {}
            with shelve.open('customer.db', 'r') as db:
                customers_dict = db.get('Customers')
                db.close()

                customer = customers_dict
                if customer:
                    customer = customers_dict.get(id)
                    update_customer_form.first_name.data = customer.get_first_name()
                    update_customer_form.last_name.data = customer.get_last_name()
                    update_customer_form.gender.data = customer.get_gender()
                    update_customer_form.email.data = customer.get_email()
                    update_customer_form.date_joined.data = customer.get_date_joined()
                    update_customer_form.address.data = customer.get_address()
                    update_customer_form.password.data = customer.get_password()

                    return render_template('updateDetails.html', form=update_customer_form)
                else:
                    return render_template('logined.html', message='Customer not found')
        except Exception as e:
            print(f"error during form pre-pop: {str(e)}")
            return render_template('logined.html', message='Error while trying to load form')


@app.route('/deleteCustomer/<id>', methods=['POST'])
def delete_customer(id):
    # delete customer information
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return render_template('home.html')


def send_message():
    user_id = request.form['user_id']
    message = request.form['message']

    # Send the user's message to SnatchBot
    api_key = '39d27725165ce5540fd6a476e502f2b0'
    endpoint = 'https://account.snatchbot.me/channels/api/api/id379991/app1234/aps1234'
    data = {'apiKey': api_key, 'user_id': user_id, 'message': message}
    response = requests.post(endpoint, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Request failed with status code {response.status_code}'}


if __name__ == '__main__':
    app.run()
