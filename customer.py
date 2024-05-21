class Customer:
    def __init__(self, customer_id, name, phone, address, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email

    def get_info(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "email": self.email
        }

    def set_info(self, name, phone, address, email):
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
