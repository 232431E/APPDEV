import hashlib
import shelve


class Login:
    # initializer method
    def _init_(self, user_id, password):
        self.__user_id = user_id
        self.__password = password

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_password(self):
        return self.__password

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_password(self, password):
        self.__password = password

    def check_password(self, password):
        return self.__password == hashlib.sha256(password.encode()).hexdigest()


class Registration(Login):
    count_id = 0

    def _init_(self, first_name, last_name, gender, email, date_joined, address, user_id, password):
        super()._init_(user_id, password)
        Registration.count_id += 1
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address

    # accessor methods
    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    # mutator methods
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _str_(self):
        return f"{self.get_user_id()}, {self.get_password()}, {self.get_first_name()}, {self.get_last_name()}"


# if _name_ == '_main_':
#     db = shelve.open('customer.db', 'r')
#     customers_dict = db['Customers']
#     db.close()

    # for key in customers_dict:
    #     customer = customers_dict.get(key)
    #     print(customer)