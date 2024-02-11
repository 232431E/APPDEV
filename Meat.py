from datetime import date


class Meats:
    count_id = 0

    def __init__(self, meat, weight, price):
        Meats.count_id += 1
        self.__id = str(Meats.count_id)
        self.__meat = meat
        self.__weight = weight
        self.__price = price
        self.__reserved = 0
        self.__bought = 0
        self.__buycount = 0
        self.__date = date.today().strftime("%d/%m/%Y")

    # Accessor methods
    def get_id(self):
        return self.__id

    def get_meat(self):
        return self.__meat

    def get_weight(self):
        return self.__weight

    def get_price(self):
        return self.__price

    def get_reserved(self):
        return self.__reserved

    def get_bought(self):
        return self.__bought

    def get_buycount(self):
        return self.__buycount

    def get_date(self):
        return self.__date

    # Mutator methods
    def set_id(self, id):
        self.__id = id

    def set_meat(self, meat):
        self.__meat = meat

    def set_weight(self, weight):
        self.__weight = weight

    def set_price(self, price):
        self.__price = price

    def set_reserved(self, reserved):
        self.__reserved = reserved

    def set_bought(self, bought):
        self.__bought = bought

    def set_buycount(self, buycount):
        self.__buycount = buycount

    def set_date(self, date):
        self.__date = date


class Users:
    count_id = 0

    def __init__(self, username, name, password, email):
        Users.count_id += 1
        self.__id = str(Users.count_id)
        self.__username = username
        self.__name = name
        self.__password = password
        self.__email = email
        self.__rmeats = []
        self.__bmeats = []

    # Accessor methods
    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_rmeats(self):
        return self.__rmeats

    def get_bmeats(self):
        return self.__bmeats

    # Mutator methods
    def set_id(self, id):
        self.__id = id

    def set_username(self, username):
        self.__username = username

    def set_name(self, name):
        self.__name = name

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_rmeats(self, rmeats):
        self.__rmeats = rmeats

    def set_bmeats(self, bmeats):
        self.__bmeats = bmeats