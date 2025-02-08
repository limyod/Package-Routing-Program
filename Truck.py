class Truck:
    def __init__(self, name, max_packages, speed,location, depart_time = None):
        self.name = name
        self.location = location
        self.max_packages = max_packages
        self.speed = speed
        self.mileage = 0
        self.depart_time = depart_time
        self.time = depart_time
        self.packages = []
    
    def at_capacity(self):
        return len(self.packages) == self.max_packages
    
    def __str__(self):
        return (f"Truck {self.name} | Location: {self.location} | "
                f"Capacity: {len(self.packages)}/{self.max_packages} | "
                f"Speed: {self.speed} units/hr | Mileage: {self.mileage} miles | "
                f"Time: {self.time} | Departed at: {self.depart_time}")