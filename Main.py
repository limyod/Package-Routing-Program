"""
Yodae Lim
012354133
main method for package routing program
"""

from datetime import datetime, timedelta
from HashTable import HashTable
from truck import Truck
from csvUtils import parse_package_from_csv, parse_distances_list_from_csv, parse_distances_matrix_from_csv

class RoutingSystem: 
    def __init__(self, package_file, distance_file, day):
        self.day = day
        #parse through packages
        self.packages_list = parse_package_from_csv(package_file)
        self.unassigned_packages = {p.package_id for p in self.packages_list}
        self.packages_map = HashTable()
        for package in self.packages_list:
            self.packages_map.set(package.package_id, package)

        #parse through addresses
        self.address_list = parse_distances_list_from_csv(distance_file)
        self.address_index_map = HashTable()
        # make look up table for later
        for i, address in enumerate(self.address_list):
            self.address_index_map.set(address, i)
        self.distance_matrix = parse_distances_matrix_from_csv(distance_file)
        
    def get_distance(self, address_index1, address_index2):
        if address_index1 >= len(self.distance_matrix) or address_index2 >= len(self.distance_matrix):
            raise ValueError("Invalid indices")
        row = max(address_index1, address_index2)
        col = min(address_index1, address_index2)
        return self.distance_matrix[row][col]

    def get_closest_package(self, location, package_id_list):
        # first find the location id
        curr_location_index = self.address_index_map.get(location)
        return min(
            package_id_list, 
            key=lambda package_id: self.get_distance(
                curr_location_index, 
                self.address_index_map.get(self.packages_map.get(package_id).address)
            )
        )

    def assign_package(self, package_id, truck):
        if(package_id not in self.unassigned_packages):
            raise ValueError("Package"+ str(package_id) + "is already assigned or doesn't exist")    
        package_location = self.packages_map.get(package_id).address
        distance = self.get_distance(self.address_index_map.get(truck.location), self.address_index_map.get(package_location))
        duration = timedelta(hours = distance / truck.speed)

        arrival_time = truck.time + duration
        deadline = self.packages_map.get(package_id).delivery_deadline
        if arrival_time > datetime.combine(self.day, deadline) :
            raise ValueError("this package id is late: " + str(package_id) +"time is:" + arrival_time.strftime('%H:%M'))
        truck.packages.append(package_id)
        truck.location = package_location
        truck.mileage += distance
        truck.time = arrival_time
        self.unassigned_packages.remove(package_id)

    #nearest neighbors algorithm for adding packages
    def assign_packages(self, package_id_list, truck):
        #get a list of unassigned packages. maybe their ids.
        unassigned_packages = package_id_list.copy()
        #get the location of truck "address"
        while not truck.at_capacity() and len(unassigned_packages) > 0:
            package_id = self.get_closest_package(truck.location, unassigned_packages)
            self.assign_package(package_id, truck)
            unassigned_packages.remove(package_id)

    def recallTruck(self, truck, hub_location):
        distance = self.get_distance(self.address_index_map.get(hub_location), self.address_index_map.get(truck.location))
        duration = timedelta(hours = distance / truck.speed)
        arrival_time = truck.time + duration
        truck.location = hub_location
        truck.mileage += distance
        truck.time = arrival_time

def main():
    """main routine for package routing""" 
    current_date = datetime.today()
    router = RoutingSystem('WGUPS Package File.csv', 'WGUPS Distance Table.csv', current_date)

    # while this would be easy if all the packages had no special instructions,
    # we realize some of the packages have deadlines, groups, known delays, and truck assignment
    # Here are a list of them.
    # 13, 14, 15, 16, 19 must be on the same truck.
    # hence, we'll consider loading all of these on truck1
    AM_packages = {1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 36, 40}
    # there are a group of delayed packages that arrive at 9:05
    delayed_packages = {6,25,28,32}
    # delayed packages 6(early), 25(early), 28, 32
    # there are a group of packages that must be on truck2
    truck2_packages = {9, 3, 36, 18}
    MAX_PACKAGES = 16
    TRUCK_SPEED = 18 # mph
    hub_address = router.address_list[0]
    truck1 = Truck("truck1", MAX_PACKAGES, TRUCK_SPEED, hub_address, current_date.replace(hour=8, minute=0, second=0, microsecond=0))
    truck3 = Truck("truck3", MAX_PACKAGES, TRUCK_SPEED, hub_address, current_date.replace(hour=9, minute=5, second=0, microsecond=0))
    truck2 = Truck("truck2", MAX_PACKAGES, TRUCK_SPEED, hub_address)
    #non-delayed, priority packages will be loaded on to the truck
    print(router.unassigned_packages)
    router.assign_packages(AM_packages, truck1)
    # we will load all the delayed_packages all together without priority because there are only four.
    router.assign_packages(delayed_packages, truck3)
    # lets fill up both trucks with the remaining packages, that do not belong on truck2
    router.assign_packages(router.unassigned_packages - truck2_packages, truck1)
    router.assign_packages(router.unassigned_packages - truck2_packages, truck3)
    # both trucks should be full or there should be no more packages left. we can recall them.
    router.recallTruck(truck1, hub_address)
    router.recallTruck(truck3, hub_address)
    truck1_return_time = truck1.time
    truck3_return_time = truck3.time
    truck2_departure_time = min(truck1_return_time, truck3_return_time)

    # Now set Truck 2's departure time
    truck2.time = truck2_departure_time
    # Assign remaining packages to Truck 2
    router.assign_packages(router.unassigned_packages, truck2)
    # recall the truck
    router.recallTruck(truck2, hub_address)
    print(len(truck1.packages) + len(truck2.packages) + len(truck3.packages))
    print(truck1.mileage + truck2.mileage + truck3.mileage)

if __name__ == "__main__":
    main()
