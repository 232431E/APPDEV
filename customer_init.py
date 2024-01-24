from flask import Flask, render_template, request
from checkoutForm import CheckoutForm
import shelve, Checkout

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('customerHome.html')

@app.route('/customerCheckout', methods=['GET', 'POST'])
def checkout():
    checkout = CheckoutForm(request.form)
    if request.method == 'POST' and checkout.validate():
        order_dict = {}
        db = shelve.open('sale.db', 'c')

    try:
        order_dict = db['Orders']
    except:
        print('Err0r in retrieving Orders from sale.db')

    order = Checkout.Checkout(checkout.collection.data, checkout.email.data, checkout.phone.data, checkout.billing_address.data,
                        checkout.date_slot.data, checkout.time_slot.data, checkout.payment.data)
    order_dict[Checkout.get._order_id()] = order
    db['Orders'] = order_dict

    db.close()

if __name__ == '__main__':
    app.run(debug=True)