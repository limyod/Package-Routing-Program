"""
main method for package routing program
"""

from datetime import datetime, timedelta
from hashTable import HashTable
from truck import Truck
from csvUtils import parse_package_from_csv, parse_distances_list_from_csv, parse_distances_matrix_from_csv

class RoutingSystem: 
    def __init__(self, package_file, distance_file, day):
        self.day = day
        #parse through packages
        self.packages_list = parse_package_from_csv(package_file)
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
        package_location = self.packages_map.get(package_id).address
        distance = self.get_distance(self.address_index_map.get(truck.location), self.address_index_map.get(package_location))
        duration = timedelta(hours = distance / truck.speed)

        arrival_time = truck.time + duration
        deadline = self.packages_map.get(package_id).delivery_deadline
        if arrival_time > datetime.combine(self.day, deadline) :
            raise ValueError("we are late.....")
        truck.packages.append(package_id)
        truck.location = package_location
        truck.mileage += distance
        truck.time = arrival_time

    #nearest neighbors algorithm for adding packages
    def assign_packages(self, package_id_list, truck):
        #get a list of unassigned packages. maybe their ids.
        unassigned_packages = package_id_list.copy()
        #get the location of truck "address"
        while not truck.at_capacity() and len(unassigned_packages) > 0:
            package_id = self.get_closest_package(truck.location, unassigned_packages)
            self.assign_package(package_id, truck)
            unassigned_packages.remove(package_id)

    def assign_all_packages(self, remaining_packages, trucks):
        for truck in trucks:
            self.assign_packages(remaining_packages, truck)
    

# def run_simulation(self, trucks, max_time, time_step=0.1):
#     current_time = 0
#     while current_time < max_time:
#         for truck in trucks:
#             if truck.

def main():
    """main routine for package routing""" 
    current_date = datetime.today()
    router = RoutingSystem('WGUPS Package File.csv', 'WGUPS Distance Table.csv', current_date)
    print(router.address_list)
    # manually add pacakges to trucks
    
    # AM packages
    # we will have one truck leave at 8am, one truck leave at 9:05, and one truck leave when the last truck returns
    # 
    MAX_PACKAGES = 16
    TRUCK_SPEED = 18 # mph
    hub_address = router.address_list[0]
    truck1 = Truck("truck1", MAX_PACKAGES, TRUCK_SPEED, hub_address, current_date.replace(hour=8, minute=0, second=0, microsecond=0))
    truck3 = Truck("truck3", MAX_PACKAGES, TRUCK_SPEED, hub_address, current_date.replace(hour=9, minute=5, second=0, microsecond=0))
    truck2 = Truck("truck2", MAX_PACKAGES, TRUCK_SPEED, hub_address)
    # we will load the AM packages that are not delayed, first. 1, 6, 13,14,15,16,20,25,
    # 13, 14, 15, 16, 19 must be on the same truck.
    #hence, we'll consider loading all of these on truck1
    AM_packages = [1, 6 ,13, 14, 15, 16, 19, 20 ,25]
    router.assign_packages(AM_packages, truck1)

    # delayed packages 6(early), 25(early), 28, 32
    delayed_packages = [6,25,28,32]
    router.assign_packages(delayed_packages, truck3)
    
    all_packages = set(router.packages_list)
    # Find unassigned packages (remaining ones)
    assigned_packages = set(AM_packages + delayed_packages)
    remaining_packages = all_packages - assigned_packages
    remaining_packages_without_truck2_designation = set(remaining_package - 
    
    # these sound like both truck 2 packages
    # we need to load "Truck2 with certain packages." 3, 36, 18 
    # package 9 is wrong address listed, corrected at 10:20am, this will be on our late truck
    truck2_packages = [9, 3, 36, 18]
    #for now lets just distribute packages without manually assignment and looking at package details
    print(truck1)
    print(truck2)
    print(truck3)


if __name__ == "__main__":
    main()
