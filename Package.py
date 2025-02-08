""" 
Package Module 

This module defines the Package class, which represents a delivery package 
with details such as address, city, state, zip code, delivery deadline, weight, and notes.
"""

class Package:
    """Class representing a package"""
    def __init__(self, package_id, address, city, state,
                 zipcode, delivery_deadline, weight_kilos, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight_kilos = weight_kilos
        self.notes = notes
        #these two fields will be updated when loaded/ delivered
        self.status = "registered"
        self.delivered_time = None

    def __str__(self):
        return (f"Package ID: {self.package_id}\n"
                f"Address: {self.address}, {self.city}, {self.state} {self.zipcode}\n"
                f"Delivery Deadline: {self.delivery_deadline}\n"
                f"Weight: {self.weight_kilos} kg\n"
                f"Notes: {self.notes}\n"
                f"Status: {self.status}\n"
                f"Delivered Time: {self.delivered_time if self.delivered_time else 'Not Delivered'}")

        
    