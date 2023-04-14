import sqlite3
from models import Employee, Location
from .animal_requests import get_single_animal

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
def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id)
        VALUES
            ( ?, ?, ?);
        """, (new_employee['name'], new_employee['address'], new_employee['location_id']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id
    return new_employee

def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Employee
        WHERE id = ?
        """, (id, ))

def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Employee
             SET
                name = ?,
                address = ?,
                location_id = ?
        WHERE id = ?
        """, (new_employee['name'], new_employee['address'], new_employee['location_id'], id, ))
        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True