class Checkout:
    order_id = 0

    def __init__(self, collection, date_slot, time_slot, payment, email, phone, address):
        Checkout.order_id += 1
        self.__order_id = Checkout.order_id
        self.__collection = collection
        self.__date_slot = date_slot
        self.__time_slot = time_slot
        self.__payment = payment
        self.__email = email
        self.__phone = phone
        self.__address = address

    def get_order_id(self):
        return self.__order_id
    def get_collection(self):
        return self.__collection
    def get_date_slot(self):
        return self.__date_slot
    def get_time_slot(self):
        return self.__time_slot
    def get_payment(self):
        return self.__payment
    def get_email(self):
        return self.__email
    def get_phone(self):
        return self.__phone
    def get_address(self):
        return self.__address


    def set_user_id(self):
        self.__order_id = Checkout.order_id
    def set_collection(self, collection):
        self.__collection = collection
    def set_date_slot(self, date_slot):
        self.__dateslot = date_slot
    def set_time_slot(self, time_slot):
        self.__timeslot = time_slot
    def set_payment(self, payment):
        self.__paymemt = payment
    def set_email(self, email):
        self.__email = email
    def set_phone(self, phone):
        self.__phone = phone
    def set_address(self, address):
        self.__address = address