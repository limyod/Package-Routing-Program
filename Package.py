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
        self.status = "registered"
        self.delivered_time = None
    