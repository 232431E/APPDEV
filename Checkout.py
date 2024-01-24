class Checkout:
    order_id = 0

    def __init__(self, collection, date_slot, time_slot, payment, email, phone, billing_address):
        Checkout.order_id += 1
        self.__order_id = Checkout.order_id
        self.__collection = collection
        self.__dateslot = date_slot
        self.__timeslot = time_slot
        self.__payment = payment
        self.__email = email
        self.__phone = phone
        self.__billing_address = billing_address

    def get_order_id(self):
        return self.__order_id
    def get_collection(self):
        return self.__collection
    def get_dateslot(self):
        return self.__dateslot
    def get_timeslot(self):
        return self.__timeslot
    def get_payment(self):
        return self.__payment
    def get_email(self):
        return self.__email
    def get_phone(self):
        return self.__phone
    def get_billingaddress(self):
        return self.__billing_address


    def set_user_id(self):
        self.__order_id = Checkout.order_id
    def set_collection(self, collection):
        self.__collection = collection
    def set_dateslot(self, date_slot):
        self.__dateslot = date_slot
    def set_timeslot(self, time_slot):
        self.__timeslot = time_slot
    def set_payment(self, payment):
        self.__paymemt = payment
    def set_email(self, email):
        self.__email = email
    def set_phone(self, phone):
        self.__phone = phone
    def set_billingaddress(self, billing_address):
        self.__billing_address = billing_address