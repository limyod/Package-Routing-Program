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
        self.load_time = None
        self.history = []

    def update_info(self, timestamp, address=None, city=None, state=None,
                    zipcode=None, notes=None):
        """Updates package details while maintaining a version history."""
            
        # Store the current state before changing it
        self.history.append({
            "timestamp": timestamp,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "notes": self.notes
        })
        
        # Apply changes only to provided fields
        if address:
            self.address = address
        if city:
            self.city = city
        if state:
            self.state = state
        if zipcode:
            self.zipcode = zipcode
        if notes:
            self.notes = notes

    def get_info_at(self, timestamp):
        """Retrieves package details at a specific time."""
        past_entries = [entry for entry in self.history if entry["timestamp"] >= timestamp]
        return past_entries[-1] if past_entries else {
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "notes": self.notes
        }

    def __str__(self):
        return (f"Package ID: {self.package_id}\n"
                f"Address: {self.address}, {self.city}, {self.state} {self.zipcode}\n"
                f"Delivery Deadline: {self.delivery_deadline}\n"
                f"Weight: {self.weight_kilos} kg\n"
                f"Notes: {self.notes}\n"
                f"Status: {self.status}\n"
                f"Delivered Time: {self.delivered_time if self.delivered_time else 'Not Delivered'}")
    