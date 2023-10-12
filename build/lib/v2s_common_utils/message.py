

def object_not_exists_message(object_name, object_id):
    """
    Generates an error message for an item with a given ID.

    Args:
        object_name (str): The name of the item.
        object_id (str): The ID of the item.

    Returns:
        A string error message.
    """
    return f"No {object_name} exists with ID {object_id}"


MESSAGES = {
    'CREATED': '{} created successfully.',
    'RETRIEVED': '{} retrieved successfully.',
    'UPDATED': '{} updated successfully.',
    'DELETED': '{} deleted successfully.',
    'UPDATE_FAILED': 'Unable to update {}.',
    'DELETE_FAILED': 'Unable to delete {}.',
    'NO_CONTENT': 'No data found.',
    'GET_ALL': '{} retrieved successfully.',
    # ... add more messages here ...
}


STATUS_MESSAGES = {
    200: 'Ok',
    201: '{} deleted successfully.',
    204: [],
    401: "You are not authorized to access this resource. Admin access required.",
    403: "You are not allowed to perform this action.",
    404: "{} Not found with id {}",
    500: "Internal Server Error",
}


LOGGER_MSG = {
    "GET_DETAILS": 'Getting {} details for ID {}.',
    "GET_ALL": 'Getting all {} data.',
    "RETRIEVED": '{} with ID {} retrieved successfully.',
    "ERROR": "An exception occurred: {}",
    "OBJECT_NOT_FOUND": "No {} details found for ID {}",
    "CREATING": "Creating a {}.",
    "CREATED": "{} created successfully with data {}.",
    "UPDATING": "Updating {} with ID {}",
    "UPDATED": "{} with ID {} updated successfully.",
    "PARTIALLY_UPDATED": "{} with ID {} partially updated successfully.",
    "DELETING": "Deleting user with ID {}.",
    "DELETED": "{} with ID {} deleted successfully.",
    'DELETE_FAILED': 'Unable to delete {}.',
    "DATA": "{} data retrieved successfully.",
    "DATA_NOT_FOUND": "No {} data found.",
}
