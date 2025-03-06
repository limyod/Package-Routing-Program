from datetime import timedelta, datetime
from csvUtils import (
    parse_package_from_csv,
    parse_distances_list_from_csv,
    parse_distances_matrix_from_csv
)
from HashTable import HashTable

class RoutingSystem:
    """
    A system for managing package deliveries using a nearest neighbor routing algorithm.

    This class handles package assignment, distance calculations, truck routing, 
    and status tracking for a package delivery service.

    Attributes:
        day (datetime.date): The current delivery date.
        packages_list (list): A list of all package objects.
        unassigned_packages (set): A set of package IDs that have not been assigned.
        packages_map (HashTable): A hash table mapping package IDs to package objects.
        address_list (list): A list of delivery addresses.
        address_index_map (HashTable): A hash table mapping addresses to index values.
        distance_matrix (list): A matrix representing distances between delivery locations.
    """

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
        """uses the distance matrix to find the distance between two address indexes."""
        if (address_index1 >= len(self.distance_matrix) or 
            address_index2 >= len(self.distance_matrix)):
            raise ValueError("Invalid indices")
        row = max(address_index1, address_index2)
        col = min(address_index1, address_index2)
        return self.distance_matrix[row][col]

    def get_closest_package(self, location, package_id_list):
        """returns the id of the nearest package,
          given a list of packages and the current location you are at"""
        curr_location_index = self.address_index_map.get(location)
        return min(
            package_id_list, 
            key=lambda package_id: self.get_distance(
                curr_location_index, 
                self.address_index_map.get(self.packages_map.get(package_id).address)
            )
        )

    def assign_package(self, package_id, truck):
        """assigns a package to a truck. most importantly updates fields of packages and trucks"""
        if package_id not in self.unassigned_packages:
            raise ValueError("Package"+ str(package_id) + "is already assigned or doesn't exist")    
        package_location = self.packages_map.get(package_id).address
        distance = self.get_distance(self.address_index_map.get(truck.location),
                                     self.address_index_map.get(package_location))
        duration = timedelta(hours = distance / truck.speed)
        arrival_time = truck.time + duration
        package = self.packages_map.get(package_id)
        deadline = package.delivery_deadline
        if arrival_time > datetime.combine(self.day, deadline) :
            raise ValueError("this package id is late: " + str(package_id) +
                             "time is:" + arrival_time.strftime('%H:%M'))
        truck.packages.append(package_id)
        truck.location = package_location
        truck.mileage += distance
        truck.time = arrival_time
        package.delivered_time = arrival_time
        package.status = "scheduled"
        package.load_time = truck.depart_time
        self.unassigned_packages.remove(package_id)

    #nearest neighbors algorithm for adding packages
    def assign_packages(self, package_id_list, truck):
        """get assign packages from a list to a truck based on the nearest neighbors algorithm"""
        #get a list of unassigned packages. maybe their ids.
        unassigned_packages = package_id_list.copy()
        #get the location of truck "address"
        while not truck.at_capacity() and len(unassigned_packages) > 0:
            package_id = self.get_closest_package(truck.location, unassigned_packages)
            self.assign_package(package_id, truck)
            unassigned_packages.remove(package_id)

    def recall_truck(self, truck, hub_location):
        """updates the truck to go back to the hub, by updating distance, time and arrival time"""
        distance = self.get_distance(self.address_index_map.get(hub_location),
                                      self.address_index_map.get(truck.location))
        duration = timedelta(hours = distance / truck.speed)
        arrival_time = truck.time + duration
        truck.location = hub_location
        truck.mileage += distance
        truck.time = arrival_time

    def get_status_for_package_id(self, package_id, query_time):
        """gets the status of a package at a given time. given a package id"""
        package = self.packages_map.get(package_id)
        return self.get_status_for_package(package, query_time)

    def get_status_for_package(self, package, query_time):
        """gets the status of a specified package at a given time"""
        status = ""
        if query_time < package.load_time:
            status = "assigned"
        elif query_time < package.delivered_time:
            status = "in transit"
        else :
            status = f"delivered at {package.delivered_time.time()}"
        package_info = package.get_info_at(query_time)
        return f"package {package.package_id:<4} | due: {package.delivery_deadline} | {status:<21} | {package_info['address']:<20} | {package.notes}"

    def get_list_package_status_at_time(self, package_id_list, query_time):
        """gets the status of all packages 
        in the list provided at the given time"""
        result = []
        for package in package_id_list:
            status = self.get_status_for_package_id(package, query_time)
            result.append(status)
        return result

    def get_truck_status(self, truck, query_time):
        """
        gets the mileage of the specified truck at the given time.
        """
        # this should get the truck mileage
        # assuming that the truck does not lose time when dropping off packages
        if query_time < truck.depart_time:
            return 0
        if query_time > truck.time:
            return truck.mileage    
        #interpolate distance traveled
        travel_time = truck.time - truck.depart_time
        travel_time_till_query = query_time - truck.depart_time
        return truck.mileage * travel_time_till_query / travel_time