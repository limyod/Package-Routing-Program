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
        package = self.packages_map.get(package_id)
        deadline = package.delivery_deadline
        if arrival_time > datetime.combine(self.day, deadline) :
            raise ValueError("this package id is late: " + str(package_id) +"time is:" + arrival_time.strftime('%H:%M'))
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

    def get_status_for_package_id(self, package_id, query_time):
        package = self.packages_map.get(package_id)
        return self.get_status_for_package(package, query_time)

    def get_status_for_package(self, package, query_time):
        status = ""
        if(query_time < package.load_time):
            status = "assigned"
        elif query_time < package.delivered_time:
            status = "in transit"
        else :
            status = f"delivered at {package.delivered_time.time()}"
        return f"package {package.package_id:<4} | {status}"
        
    def get_list_package_status_at_time(self, package_id_list, query_time):
        result = []
        for package in package_id_list:
            status = self.get_status_for_package_id(package, query_time)
            result.append(status)
        return result
    
    def get_truck_status(self, truck, query_time):
        # this should get the truck mileage
        # assuming that the truck does not lose time when dropping off packages
        if(query_time < truck.depart_time):
            return 0
        
        if(query_time > truck.time):
            return truck.mileage
        
        #interpolate distance traveled
        travel_time = truck.time - truck.depart_time
        travel_time_till_query = query_time - truck.depart_time
        return truck.mileage * travel_time_till_query / travel_time
        

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
    trucks = [truck1, truck2, truck3]
    #non-delayed, priority packages will be loaded on to the truck
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

    # lets update the address of package # 9.
    package_9 = router.packages_map.get(9)
    package_9.address = '410 S State St'
    package_9.city = 'Salt Lake City'
    package_9.state = 'UT'
    package_9.zipcode = '84111'
    # Now set Truck 2's departure time. it'll be 9:30 to match the update, or when the first truck comes back. whichever is later
    truck2_departure_time = max(min(truck1_return_time, truck3_return_time), current_date.replace(hour=9, minute=30, second=0, microsecond=0))
    truck2.depart_time = truck2_departure_time
    truck2.time = truck2_departure_time
    
    # Assign remaining packages to Truck 2
    router.assign_packages(router.unassigned_packages, truck2)
    # recall the truck
    router.recallTruck(truck2, hub_address)

    ### this is the CLI section
    print('Welcome to the Package Status Viewer!')
    print('-' * 50)
    print("Here are some delivery stats:\n")
    print(f"Total mileage traveled by all trucks: {truck1.mileage + truck2.mileage + truck3.mileage:.2f} miles")
    
    print("\nTruck statuses:")
    for truck in trucks:
        print(truck)
    
    print('-' * 50)
    while True:
        package_input = input('Enter a package id or press Enter to view all packages (or type "quit" to exit): ').strip()

        if package_input.lower() == 'quit':
                print("Exiting the program...")
                break

        if package_input and (not package_input.isdigit() or int(package_input) not in router.packages_map.keys()):
            print("That is not a valid package id")
            continue

        # Get time input
        time_input = input('Enter a time to check the status (HH:MM): ').strip()
        try:
            time_object = datetime.strptime(time_input, "%H:%M")
            today = datetime.today().date()
            query_date_time = datetime.combine(today, time_object.time())
        except ValueError:
            print("Invalid time format. Please enter time in HH:MM format.")
            continue

        # Show package status based on input
        if package_input == '':
            print("Package and truck status:")
            total_truck_mileage = 0
            for truck in trucks:
                mileage = router.get_truck_status(truck, query_date_time)
                total_truck_mileage += mileage

                print(f"\n========= {truck.name} =========")
                print(f"Total mileage at {query_date_time.time()} is {mileage} miles")
                statuses = router.get_list_package_status_at_time(truck.packages, query_date_time)
                print("\n".join(statuses))
            unassigned_num = len(router.unassigned_packages)
            print(f"\nThere are {unassigned_num} packages that are not assigned\n")
            print(f"Trucks have traveled a total of {total_truck_mileage} miles at {query_date_time.time()}")
        else:
            print(router.get_status_for_package_id(int(package_input), query_date_time))
            print()

        print('-' * 50)

if __name__ == "__main__":
    main()
