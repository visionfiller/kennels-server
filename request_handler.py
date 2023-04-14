import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import create_animal, delete_animal, get_all_animals, get_single_animal, update_animal, get_animal_by_word
from views import create_location, get_all_locations, get_single_location, delete_location, update_location
from views import create_employee, get_all_employees, get_single_employee, delete_employee, update_employee
from views import get_all_customers, get_single_customer, create_customer, update_customer


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
method_mapper = {
    "animals":{
        "single": get_single_animal,
        "all": get_all_animals
        },
    "locations": {
        "single":get_single_location,
        "all": get_all_locations
    },
    "employees": {
        "single": get_single_employee,
        "all":get_all_employees
    },
    "customers": {
        "single":get_single_customer,
        "all" : get_all_customers
    }
}
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response

    def do_GET(self):
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        if '?'  not in self.path:
            self._set_headers(200)
            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals(query_params)
            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
        else:
            self._set_headers(200)
            if query_params.get('search'):
                    response = get_animal_by_word(query_params['search'][0])
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
       
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            self._set_headers(201)
            new_animal = create_animal(post_body)
            self.wfile.write(json.dumps(new_animal).encode())
        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create_location(post_body)
            else:
                 self._set_headers(400)
                 new_location = { "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'}
            self.wfile.write(json.dumps(new_location).encode())
        if resource == "employees":
            self._set_headers(201)
            new_employee = create_employee(post_body)
            self.wfile.write(json.dumps(new_employee).encode())
        if resource == "customers":
            self._set_headers(201)
            new_customer = create_customer(post_body)
            self.wfile.write(json.dumps(new_customer).encode())
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id, query_params) = self.parse_url(self.path)
        if resource == "animals":
            success = update_animal(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())
        if resource == "locations":
            success= update_location(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())
        if resource == "employees":
            success = update_employee(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())
        if resource == "customers":
            success= update_customer(id, post_body)
            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)
        self.wfile.write("".encode())
    
    def do_DELETE(self):
        (resource, id, query_params) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            self._set_headers(204)
            delete_animal(id)
        if resource == "locations":
            self._set_headers(204)
            delete_location(id)
        if resource == "employees":
            self._set_headers(204)
            delete_employee(id)
        if resource == "customers":
            self._set_headers(405)
            response = { "message": "Cannot Delete Customers" }
        if response is not None:
              self.wfile.write(json.dumps(response).encode())
        else:
             self.wfile.write("".encode())
    # Encode the new animal and send in response
        

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = parse_qs(url_components.query)

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)
# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
