import sqlite3
from models import Employee, Location
from views import get_single_animal

def get_all_employees():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

       
        db_cursor.execute("""
        SELECT DISTINCT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address,
            (
           SELECT GROUP_CONCAT(a.id)
            FROM AnimalsAssignedtoEmployee t
            JOIN Animal a ON t.animal_id = a.id
            WHERE t.employee_id = e.id) as animals_assigned
            FROM Employee e
            JOIN Location l
                ON l.id = e.location_id
            LEFT OUTER JOIN AnimalsAssignedtoEmployee t
                    ON t.employee_id = e.id
            LEFT OUTER JOIN Animal a
                    ON t.animal_id = a.id
       """)
       
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            employee = Employee(row['id'],row['name'], row['address'], row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            animals_assigned = row['animals_assigned'].split(",") if row['animals_assigned'] else []
            assignments= []
            for assignment in animals_assigned:
                assignment_object = get_single_animal(assignment)
                assignments.append(assignment_object)
            employee.animals = assignments
            employees.append(employee.__dict__)
        return employees

# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
         SELECT DISTINCT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address,
            (
           SELECT GROUP_CONCAT(a.id)
            FROM AnimalsAssignedtoEmployee t
            JOIN Animal a ON t.animal_id = a.id
            WHERE t.employee_id = e.id) as animals_assigned
            FROM Employee e
            JOIN Location l
                ON l.id = e.location_id
            LEFT OUTER JOIN AnimalsAssignedtoEmployee t
                    ON t.employee_id = e.id
            LEFT OUTER JOIN Animal a
                    ON t.animal_id = a.id
            WHERE e.id = ?
        """, (id, ))

        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'],row['name'], row['address'], row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            animals_assigned = row['animals_assigned'].split(",") if row['animals_assigned'] else []
            assignments= []
            for assignment in animals_assigned:
                assignment_object = get_single_animal(assignment)
                assignments.append(assignment_object)
            employee.animals = assignments
    
          
        return employee.__dict__
def create_employee(employee):
    # Get the id value of the last animal in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    employee["id"] = new_id

    # Add the animal dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    # Initial -1 value for animal index, in case one isn't found
    employee_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the animal. Store the current index.
            employee_index = index

    # If the animal was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the animal. Update the value.
            EMPLOYEES[index] = new_employee
            break