"""
main method for package routing program
"""

from package import Package
from hashTable import HashTable
from truck import Truck
from csvUtils import parse_package_from_csv, parse_distances_list_from_csv, parse_distances_matrix_from_csv

class RoutingSystem: 
    def __init__(self, package_file, distance_file):
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
        row = min(address_index1, address_index2)
        col = max(address_index1, address_index2)
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
        duration = distance/ truck.speed
        truck.packages.append(package_id)
        truck.location = package_location
        truck.mileage += distance
        truck.time += distance / truck.speed

    #nearest neighbors algorithm for adding packages
    def assign_packages(self, package_id_list, truck):
        #get a list of unassigned packages. maybe their ids.
        unassigned_packages = package_id_list.clone()
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
    
    router = RoutingSystem('WGUPS Package File.csv', 'WGUPS Distance Table.csv')
    # manually add pacakges to trucks
    remaining_packages = router.packages_list.copy()
    
    # AM packages
    # we will have one truck leave at 8am, one truck leave at 9:05, and one truck leave when the last truck returns
    # 
    # we will load the AM packages that are not delayed, first. 1, 6, 13,14,15,16,20,25,

    # 13, 14, 15, 16, 19 must be on the same truck.

    # we need to load "Truck2 with certain packages." 3, 18, 

    # delayed packages 6, 25, 28, 32
    
    # package 9 is wrong address listed, corrected at 10:20am, this will be on our late truck

    #for now lets just distribute packages without manually assignment and looking at package details


if __name__ == "__main__":
    main()
