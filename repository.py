DATABASE = {
    "animals": [
        {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
    ], 
    "customers": [
        {
        "id": 1,
        "name": "Ryan Tanay"
    },
    {
        "id": 2,
        "name": "Vision Filler"
    }
    ],
    "employees": [
    {
        "id": 1,
        "name": "Jenna Solis"
    },
    {
        "id": 2,
        "name": "Bob Bobertson"
    }
],
"locations": [
     {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]
    }

def all(resources):
    """For GET requests to collection"""
    return DATABASE[resources]



def retrieve(resources, id):
    """For GET requests to a single resource"""
    requested_resource = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for resource in DATABASE[resources]:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if resource["id"] == id:
            requested_resource= resource

    return requested_resource


def create(resources, resource):
    """For POST requests to a collection"""
    max_id = DATABASE[resources][-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    resource["id"] = new_id

    # Add the animal dictionary to the list
    DATABASE[resources].append(resource)

    # Return the dictionary with `id` property added
    return resource


def update(id, new_resource, resources):
    """For PUT requests to a single resource"""
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            # Found the animal. Update the value.
            DATABASE[resources][index] = new_resource
            break


def delete(resources, id):
    """For DELETE requests to a single resource"""
        # Initial -1 value for animal index, in case one isn't found
    resource_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            # Found the animal. Store the current index.
            resource_index = index

    # If the animal was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[resources].pop(resource_index)