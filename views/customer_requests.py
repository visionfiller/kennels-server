import sqlite3
from models import Customer

def get_all_customers():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

       
        db_cursor.execute("""
        SELECT
            c.id,
            c.name name,
            c.address address,
            c.email,
            c.password
        FROM Customer c
       """)
       
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            customer = Customer(row['id'],row['name'], row['address'], row['email'], row['password'])
           
            customers.append(customer.__dict__)
        return customers

# Function with a single parameter
def get_single_customer(id):
   with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

       
        db_cursor.execute("""
        SELECT
            c.id,
            c.name name,
            c.address address,
            c.email,
            c.password
        FROM Customer c
        WHERE c.id = ?
       """, ( id, ))
        data = db_cursor.fetchone()
        customer = Customer(data['id'],data['name'], data['address'], data['email'], data['password'])
        return customer.__dict__

def create_customer(new_customer):
   with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Customer
            ( name, address, email, password)
        VALUES
            ( ?, ?, ?, ?);
        """, (new_customer['name'], new_customer['address'], new_customer['email'], new_customer['password']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_customer['id'] = id
        return new_customer

def delete_customer(id):
   with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Customer
        WHERE id = ?
        """, (id, ))

def update_customer(id, new_customer):
     with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Customer
             SET
                name = ?,
                status = ?,
                breed = ?,
                customer_id,
                location_id   
        WHERE id = ?
        """, (new_customer['name'], new_customer['address'], new_customer['email'], new_customer['password'], id, ))
        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True