"""
main method for package routing program
"""

import csv
from package import Package

def parse_package_from_csv(csv_filename):
    """method returning a list of packages given a csv with packages"""
    package_list = []
    with open(csv_filename, encoding='utf-8',  mode='r') as file:
        csv_file = csv.DictReader(file)
        csv_file.fieldnames = [name.replace("\n", " ").strip() for name in csv_file.fieldnames]
        for package_line in csv_file:
            package_list.append(Package(
                package_line['Package ID'],
                package_line['Address'],
                package_line['City'],
                package_line['State'],
                package_line['Zip'],
                package_line['Delivery Deadline'],
                package_line['Weight KILO'],
                package_line['page 1 of 1PageSpecial Notes']
            ))
    return package_list

def parse_distances_list_from_csv(csv_filename):
    """method returning a list of addresses"""
    address_list = []
    with open(csv_filename, encoding='utf-8',  mode='r') as file:
        csv_file = csv.reader(file)
        # skip the first row, as it contains the full addresses which are harder to work with.
        # use the 2nd column instead.
        next(csv_file)
        for row in csv_file:
            address = row[1].splitlines()[0].strip()
            address_list.append(address)
    return address_list

def parse_distances_matrix_from_csv(csv_filename):
    """method returning a distance matrix"""
    


#parse_package_from_csv('WGUPS Package File.csv')
#parse_distances_list_from_csv('WGUPS Distance Table.csv')
