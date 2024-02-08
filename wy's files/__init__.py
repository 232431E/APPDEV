from flask import Flask, render_template, session, url_for, request, redirect, flash
from flask_session import Session
from Forms import *
from Meat import *
import shelve

app = Flask(__name__, template_folder='templates')
app.secret_key = 'my_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

meatlst = [
    Meats('Chicken Breast', '500g', '$5.99'),
    Meats('Marinated Chicken Wings', '800g', '$8.99'),
    Meats('Mojito Grilled Chicken Breast', '550g', '$12.99'),
    Meats('Salmon Fillet', '400g', '$11.99'),
    Meats('Pineapple Teriyaki Salmon', '600g', '$15.99'),
    Meats('Venison Steak', '500g', '$19.99'),
    Meats('Garlic Butter Steak Tips', '800g', '$16.99'),
    Meats('Pork Ribs', '750g', '$12.99'),
    Meats('Chipotle Lime Pork Tenderloin', '650g', '$11.49'),
    Meats('Tiger Shrimp', '500g', '$15.99'),
    Meats('Spicy Cajun Shrimp Skewers', '450g', '$13.49'),

]

with shelve.open('library.db', 'c') as db:
    if 'Meats' not in db:
        db['Meats'] = {}
    library = db['Meats']
    for meat in meatlst:
        library[meat.get_id()] = meat
    db['Meats'] = library

with shelve.open('users.db', 'c') as db:
    if 'Users' not in db:
        db['Users'] = {}


@app.route('/')
def main():
    return render_template('mainpage.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup = signupForm(request.form)
    if request.method == 'POST' and signup.validate():
        users = {}
        with shelve.open('users.db', 'c') as db:
            users = db['Users']
            new = Users(signup.username.data, signup.name.data, signup.password.data, signup.email.data)
            if new.get_username() in users:
                return redirect(url_for('login'))
            else:
                users[new.get_username()] = new
            db['Users'] = users
            db.sync()

        return redirect(url_for('home'))

    return render_template('signup.html', form=signup)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = loginForm(request.form)
    if request.method == 'POST' and login.validate():
        with shelve.open('users.db', 'c') as db:
            users = db['Users']
            for user in users.values():
                if user.get_username() == login.username.data and user.get_password() == login.password.data:
                    session['logged_in'] = True
                    session['username'] = user.get_username()
                    return redirect(url_for('home'))
            return render_template('failedlogin.html')

    return render_template('login.html', form=login)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('main'))


@app.route('/updateProfile', methods=['GET', 'POST'])
def update_profile():
    update_form = updateProfileForm(request.form)
    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        current_user = users[session['username']]
        if request.method == 'POST' and update_form.validate():
            with shelve.open('users.db', 'c') as db:
                users = db['Users']
                current_user = users[session['username']]
                current_user.set_username(update_form.username.data)
                current_user.set_name(update_form.name.data)
                current_user.set_email(update_form.email.data)
                users[current_user.get_username()] = current_user
                session['username'] = current_user.get_username()
                users[session['username']] = current_user
                db['Users'] = users
                db.sync()

                return render_template("updateSuccess.html", form=update_form, name_to_update=current_user)

        return render_template('updateProfile.html', form=update_form, current_user=current_user)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        current_user = users[session['username']]

    return render_template('dashboard.html', current_user=current_user)


@app.route('/confirm_delete')
def confirm_delete():
    return render_template('confirmDelete.html')


@app.route('/delete')
def delete():
    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        current_user = users[session['username']]
        session['username'] = current_user.get_username()
        users[session['username']] = current_user

        users.pop(current_user.get_username())

        db['Users'] = users
        db.close()

    return redirect(url_for('main'))


@app.route('/home')
def home():
    if 'logged_in' not in session or session['logged_in'] != True:
        return redirect(url_for('login'))
    else:

        with shelve.open('library.db', 'r') as db:
            library = db['Meats']
            meats = []
            popular = {}
            for meat in library:
                if library[meat].get_reserved() == 0:
                    meats.append(library[meat])
                popular[library[meat].get_id()] = library[meat].get_buycount()

        meats.sort(key=lambda x: int(x.get_id()))
        popular = sorted(popular.items(), key=lambda x: x[1], reverse=True)
        top = []
        print("Popular:", popular)
        if len(popular) >= 5:
            for i in range(5):
                meat_id = popular[i][0]
                meat = library.get(meat_id)  # Use get() to avoid KeyError
                top.append(meat)
        else:
            print("Not enough elements in 'popular' list.")

        with shelve.open('users.db', 'r') as db:
            users = db['Users']
            name = session.get('username', '')
            boughtlst = users[name].get_bmeats()

        return render_template('home.html', meats=meats, boughtlst=boughtlst, top=top)


@app.route('/reserveMeat/<int:id>', methods=['POST', 'GET'])
def reserveMeat(id):
    library = {}

    users = {}
    name = session.get('username', '')
    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        newlst = users[name].get_rmeats()
        if len(newlst) < 5:
            users[name].set_rmeats(newlst)

            with shelve.open('library.db', 'c') as data:
                library = data['Meats']
                library[str(id)].set_reserved(1)
                data['Meats'] = library
            newlst.append(library[str(id)].get_id())
            db['Users'] = users
        else:
            return render_template('excess.html')
    return redirect(url_for('home'))


@app.route('/reserved')
def reserved():
    with shelve.open('library.db', 'r') as db:
        with shelve.open('users.db', 'r') as udb:
            library = db['Meats']
            users = udb['Users']
            name = session.get('username', '')
            reservedlst = []
            for meat in library:
                if library[meat].get_id() in users[name].get_rmeats():
                    reservedlst.append(library[meat])

    reservedlst.sort(key=lambda x: int(x.get_id()))

    if len(reservedlst) == 0:
        return render_template('reservedempty.html')

    return render_template('reserved.html', meats=reservedlst)


@app.route('/cancelReserve/<int:id>', methods=['POST', 'GET'])
def cancelReserved(id):
    with shelve.open('library.db', 'c') as db:
        library = db['Meats']
        library[str(id)].set_reserved(0)
        db['Meats'] = library

    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        name = session.get('username', '')
        lst = users[name].get_rmeats()
        lst.pop(lst.index(str(id)))
        users[name].set_rmeats(lst)
        db['Users'] = users

    return redirect(url_for('reserved'))


@app.route('/buyMeat/<int:id>', methods=['GET', 'POST'])
def buyMeat(id):
    library = {}
    users = {}
    name = session.get('username', '')
    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        newlst = users[name].get_bmeats()
        if len(newlst) < 5:
            users[name].set_bmeats(newlst)
            with shelve.open('library.db', 'c') as data:
                library = data['Meats']
                library[str(id)].set_bought(1)
                due = library[str(id)].get_date().split('/')
                month = str(int(due[1]) + 1)
                due[1] = month
                if len(due[1]) == 1:
                    due[1] += '0'
                    due[1] = due[1][::-1]
                library[str(id)].set_date('/'.join(due))
                bcount = library[str(id)].get_buycount()
                library[str(id)].set_buycount(bcount + 1)
                data['Meats'] = library
            newlst.append(library[str(id)].get_id())
            db['Users'] = users
        else:
            return render_template('excess.html')
    print(newlst)
    return redirect(url_for('home'))


@app.route('/bought')
def bought():
    with shelve.open('library.db', 'c') as db:
        with shelve.open('users.db', 'r') as udb:
            library = db['Meats']
            users = udb['Users']
            name = session.get('username', '')
            boughtlst = []
            for meat in library:
                if library[meat].get_id() in users[name].get_bmeats():
                    boughtlst.append(library[meat])

    boughtlst.sort(key=lambda x: int(x.get_id()))

    if len(boughtlst) == 0:
        return render_template('boughtempty.html')

    return render_template('bought.html', meats=boughtlst)


@app.route('/cancelBought/<int:id>', methods=['POST', 'GET'])
def cancelBought(id):
    with shelve.open('library.db', 'c') as db:
        library = db['Meats']
        library[str(id)].set_bought(0)
        library[str(id)].set_date(date.today().strftime("%d/%m/%Y"))
        with shelve.open('users.db', 'c') as data:
            if library[str(id)].get_reserved() == 1:
                users = data['Users']
                for user in users:
                    if library[str(id)].get_id() in users[user].get_rmeats():
                        blst = users[user].get_bmeats()
                        blst.append(library[str(id)].get_id())
                        users[user].set_bmeats(blst)
                        rlst = users[user].get_rmeats()
                        rlst.pop(rlst.index(library[str(id)].get_id()))
                        users[user].set_rmeats(rlst)
                        library[str(id)].set_bought(1)
                        library[str(id)].set_reserved(0)
                        due = library[str(id)].get_date().split('/')
                        month = str(int(due[1]) + 1)
                        due[1] = month
                        if len(due[1]) == 1:
                            due[1] += '0'
                            due[1] = due[1][::-1]
                        library[str(id)].set_date('/'.join(due))
                        data['Users'] = users
        db['Meats'] = library

    with shelve.open('users.db', 'c') as db:
        users = db['Users']
        name = session.get('username', '')
        lst = users[name].get_bmeats()
        lst.pop(lst.index(str(id)))
        users[name].set_bbooks(lst)
        db['Users'] = users

    return redirect(url_for('bought'))


@app.route('/requestMeat', methods=['GET', 'POST'])
def requestMeat():
    request_meat = requestMeatForm(request.form)
    if request.method == 'POST' and request_meat.validate():
        library = {}
        with shelve.open('library.db', 'c') as db:
            library = db['Meats']
            meat = Meats(request_meat.meat.data, request_meat.weight.data, request_meat.price.data)
            library[meat.get_id()] = meat
            db['Meats'] = library

        return redirect(url_for('home'))
    return render_template('request.html', form=request_meat)


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    with shelve.open('library.db', 'r') as db:
        library = db['Meats']
        results = []
        for meat in library:
            if query.lower() == 'all':
                return redirect(url_for('home'))
            elif query.lower() == str(library[meat].get_meat()).lower() or query.lower() == str(library[meat].get_weight()).lower() or query.lower() == str(library[meat].get_price()).lower():
                results.append(library[meat])
            elif 'id:' in query.lower():
                id = query[3:]
                if id == str(library[meat].get_id()):
                    results.append(library[meat])

    return render_template('search_results.html', results=results, query=query)


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    with shelve.open('forum_data') as data:
        if request.method == 'POST':
            name = session.get('username', '')
            message = request.form['message']
            messages = data.get('messages', [])
            messages.append({
                'id': len(messages) + 1,
                'name': name,
                'message': message,
                'replies': []
            })
            data['messages'] = messages
            return redirect(url_for('forum'))
        else:
            messages = data.get('messages', [])
            return render_template('forum.html', messages=messages, username=session.get('username', ''))


@app.route('/addmessage')
def add_message():
    return render_template('addmessage.html')


@app.route('/forum/update/<int:message_id>', methods=['POST'])
def update_message(message_id):
    with shelve.open('forum_data') as data:
        messages = data.get('messages', [])
        if message_id - 1 < len(messages):
            message = messages[message_id - 1]
            message['name'] = session.get('username', '')
            message['message'] = request.form['message']
            data['messages'] = messages
            return redirect(url_for('forum'))
        else:
            return "Message not found", 404


@app.route('/forum/edit/<int:message_id>', methods=['GET'])
def edit_message(message_id):
    with shelve.open('forum_data') as data:
        messages = data.get('messages', [])
        if message_id - 1 < len(messages):
            message = messages[message_id - 1]
            return render_template('edit_message.html', message=message, message_id=message_id)
        else:
            return "Message not found", 404


@app.route('/forum/delete/<int:message_id>', methods=['GET'])
def delete_message(message_id):
    with shelve.open('forum_data') as data:
        messages = data.get('messages', [])
        if message_id - 1 < len(messages):
            del messages[message_id - 1]
            data['messages'] = messages
            return redirect(url_for('forum'))
        else:
            return "Message not found", 404


@app.route('/forum/add_reply/<int:message_id>', methods=['GET', 'POST'])
def add_reply(message_id):
    with shelve.open('forum_data') as data:
        messages = data.get('messages', [])
        if message_id - 1 < len(messages):
            message = messages[message_id - 1]
            if request.method == 'POST':
                name = session.get('username', '')
                reply_message = request.form['message']
                message['replies'].append({
                    'name': name,
                    'message': reply_message
                })
                data['messages'] = messages
                return redirect(url_for('forum'))
            else:
                return render_template('add_reply.html', message_id=message_id)
        else:
            return "Message not found", 404


if __name__ == "__main__":
    app.debug = True
    app.run()
