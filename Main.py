"""
Yodae Lim
012354133
main method for package routing program
"""

from datetime import datetime
from truck import Truck
from RoutingSystem import RoutingSystem

def main():
    """main routine for package routing""" 
    current_date = datetime.today()
    router = RoutingSystem('WGUPS Package File.csv', 'WGUPS Distance Table.csv', current_date)

    # while this would be easy if all the packages had no special instructions,
    # we realize some of the packages have deadlines, groups, known delays, and truck assignment
    # Here are a list of them.
    # 13, 14, 15, 16, 19 must be on the same truck.
    # hence, we'll consider loading all of these on truck1
    AM_packages = {1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 40}
    # there are a group of delayed packages that arrive at 9:05
    delayed_packages = {6,25,28,32}
    # delayed packages 6(early), 25(early), 28, 32
    # there are a group of packages that must be on truck2
    truck2_packages = {9, 3, 36, 38, 18}
    MAX_PACKAGES = 16
    TRUCK_SPEED = 18 # mph
    hub_address = router.address_list[0]
    truck1 = Truck("truck1", MAX_PACKAGES, TRUCK_SPEED, hub_address, 
                   current_date.replace(hour=8, minute=0, second=0, microsecond=0))
    truck3 = Truck("truck3", MAX_PACKAGES, TRUCK_SPEED, hub_address, 
                   current_date.replace(hour=9, minute=5, second=0, microsecond=0))
    truck2 = Truck("truck2", MAX_PACKAGES, TRUCK_SPEED, hub_address)
    trucks = [truck1, truck2, truck3]
    #non-delayed, priority packages will be loaded on to the truck
    router.assign_packages(AM_packages, truck1)
    # we will load all the delayed_packages all 
    # together without priority because there are only four.
    router.assign_packages(delayed_packages, truck3)
    # lets fill up both trucks with the remaining packages, that do not belong on truck2
    router.assign_packages(router.unassigned_packages - truck2_packages, truck1)
    router.assign_packages(router.unassigned_packages - truck2_packages, truck3)
    # both trucks should be full or there should be no more packages left. we can recall them.
    router.recall_truck(truck1, hub_address)
    router.recall_truck(truck3, hub_address)
    truck1_return_time = truck1.time
    truck3_return_time = truck3.time

    # lets update the address of package # 9.
    package_9 = router.packages_map.get(9)
    package_9.address = '410 S State St'
    package_9.city = 'Salt Lake City'
    package_9.state = 'UT'
    package_9.zipcode = '84111'
    # Now set Truck 2's departure time. it'll be 9:30 to match the update, 
    # or when the first truck comes back. whichever is later
    truck2_departure_time = max(min(truck1_return_time, truck3_return_time),
                                 current_date.replace(hour=9, minute=30, second=0, microsecond=0))
    truck2.depart_time = truck2_departure_time
    truck2.time = truck2_departure_time

    # Assign remaining packages to Truck 2
    router.assign_packages(router.unassigned_packages, truck2)
    # recall the truck
    router.recall_truck(truck2, hub_address)

    ### this is the CLI section
    print('Welcome to the Package Status Viewer!')
    print('-' * 50)
    print("Here are some delivery stats:\n")
    print("Total mileage traveled by all trucks: "
          f"{truck1.mileage + truck2.mileage + truck3.mileage:.2f} miles")
    print("\nTruck statuses:")
    for truck in trucks:
        print(truck)

    print('-' * 50)
    while True:
        package_input = input('Enter a package id or press Enter '
                              'to view all packages (or type "quit" to exit): ').strip()

        if package_input.lower() == 'quit':
            print("Exiting the program...")
            break

        if package_input and (not package_input.isdigit() or
                               not router.packages_map.contains_key(int(package_input))):
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
            print(f"Trucks have traveled a total of {total_truck_mileage} miles "
                  f"at {query_date_time.time()}")
        else:
            print(router.get_status_for_package_id(int(package_input), query_date_time))
            print()

        print('-' * 50)

if __name__ == "__main__":
    main()
