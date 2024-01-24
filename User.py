# User class
class User:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name, gender, position, email, phone):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__position = position
        self.__email = email
        self.__phone = phone

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_position(self):
        return self.__position

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_position(self, position):
        self.__position = position

    def set_email(self, email):
        self.__remarks = email

    def set_phone(self, phone):
        self.__phone = phone