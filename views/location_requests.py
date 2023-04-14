import sqlite3
from models import Location, Employee

def get_all_locations():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

       
        db_cursor.execute("""
        SELECT
            l.id,
            l.name name,
            l.address address,
            COUNT(*) AS animals
        FROM Location l
        JOIN Animal a ON l.id = a.location_id
        GROUP BY a.location_id
        
       """)
       
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            location = Location(row['id'],row['name'], row['address'])
            location.animals = row['animals']
            locations.append(location.__dict__)
        return locations

# Function with a single parameter
def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
         SELECT DISTINCT
            l.id,
            l.name location_name,
            l.address location_address,
            (
           SELECT GROUP_CONCAT(a.name)
                FROM Animal a WHERE a.location_id = l.id) as animals_assigned,
                (
            SELECT GROUP_CONCAT(e.name)
                FROM Employee e WHERE e.location_id = l.id) as employees_assigned
            FROM Location l
            LEFT JOIN Employee e
                ON l.id = e.location_id
            LEFT OUTER JOIN Animal a
                    ON a.location_id = l.id
        WHERE l.id = ?;
        """, ( id, ))

        dataset = db_cursor.fetchall()
        for row in dataset:
            location = Location(row['id'], row['location_name'], row['location_address'])
            animals_assigned = row['animals_assigned'].split(",") if row['animals_assigned'] else []
            assignments= []
            for assignment in animals_assigned:
                assignments.append(assignment)
            location.animals = assignments
            employees_assigned = row['employees_assigned'].split(",") if row['employees_assigned'] else []
            employee_assignments= []
            for assignment in employees_assigned:
                employee_assignments.append(assignment)
            location.employees = employee_assignments
          
        return location.__dict__

def create_location(new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Location
            ( name, address)
        VALUES
            ( ?, ?);
        """, (new_location['name'], new_location['status']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_location['id'] = id
    return new_location

def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Location
        WHERE id = ?
        """, (id, ))

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Location
             SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id, ))
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
            # Forces 404 response by main module
        return False
    else:
            # Forces 204 response by main module
        return True