from collections import namedtuple
import requests
from bs4 import BeautifulSoup


BASE_URL = "http://wpvitassuds01.itap.purdue.edu/washalertweb/washalertweb.aspx"
LOCATION_SPECIFIC_URL = BASE_URL + "?location="

LaundryLocation = namedtuple('LaundryLocation', ['name', 'uuid'])


def get_locations():
    """Returns a list of LaundryLocations
    """
    locations = []

    page_content = requests.get(BASE_URL).text
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find the <select id="locationSelector">
    location_selector = soup.find("select", id="locationSelector")

    # Iterate over the children of the select
    for option in location_selector:
        # Ignore everything that isn't an <option>
        if option.name != "option":
            continue

        # The name is the text of the option, for example
        # <option value="...">12345</option>
        name = option.string.strip()
        # The id of the laundry location is the value attribute of the <option>
        locations.append(LaundryLocation(name, option['value']))

    return locations


def location_status(location_id):
    page_content = requests.get(LOCATION_SPECIFIC_URL + location_id).text
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find the first table on the page
    table = soup.find('table')

    laundry_machines = []

    # Iterate over every row in the table
    for row in table.find_all('tr'):
        machine = {}

        # Get all the elements in the table
        elements = row.find_all('td')
        for element in elements:
            # Get the class attribute of the element,
            # the easiest way to get each attribute of
            # a laundry machine
            element_class = element.get('class')
            # We only care about the first class.
            # The page doesn't even have multiple classes
            # in a single tag
            #
            # e.g <div class="class1 class2">
            if element_class:
                element_class = element_class[0]

            if element_class == 'name':
                if element.img:
                    element.img.decompose()
                machine['name'] = element.string
            elif element_class == 'type':
                machine['type'] = element.string
            elif element_class == 'status':
                machine['status'] = element.string
            elif element_class == 'time':
                if machine['status'] == 'In use':
                    if element.div:
                        element.div.decompose()
                    machine['time'] = element.string
            elif element_class == 'form':
                if machine['status'] == 'In use':
                    control_id_attrs = {'name': "controlid"}
                    control_id = element.find('input', control_id_attrs).get('value')
                    machine['control_id'] = control_id

        # Only add the machine if the 3 required attributes,
        # name, type and status are available
        if 'name' in machine and 'type' in machine and 'status' in machine:
            laundry_machines.append(machine)

    return laundry_machines

def scrape_all():
    all_machines = {}
    for location in get_locations():
        print "[!] Scraping " + location.name

        all_machines[location.name] = location_status(location.uuid)

    return all_machines
