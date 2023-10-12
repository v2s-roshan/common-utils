import base64
import json
import random
import string
import uuid
import re
from datetime import datetime
from uuid import UUID

from django.core.files import File
from django.db.models.fields.files import FieldFile

from rest_framework.response import Response
from rest_framework import serializers








def file_to_blob(file_path):
    """
    Converts a file at the given file path to a base64-encoded string.

    Args:
        file_path (str): The absolute path to the file to convert.

    Returns:
        A base64-encoded string of the file contents, or None if the file could not be found.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            encoded_data = base64.b64encode(data).decode('utf-8')
            return encoded_data
    except FileNotFoundError:
        return None





def generate_random_username(length=8):
    """Generate a random username."""
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

def generate_random_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password



def genrate_unique_number():
    # Generate a unique UUID (Universally Unique Identifier)
    unique_id = uuid.uuid4()

    # Convert the UUID to a string and remove hyphens to create a unique number
    unique_number = str(unique_id).replace('-', '')

    return unique_number


def generate_otp():
    # Generate a 6-digit random number
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp




# def create_django_file(filepath):
#     """
#     Creates a Django File object from the given filepath.

#     Args:
#         filepath (str): The path to the file.

#     Returns:
#         object: The created Django File object.

#     Raises:
#         FileNotFoundError: If the file is not found.
#         IOError: If an error occurs while reading the file.
#         FileObjectCreationError: If an error occurs during the process of creating the Django File object.
#     """
#     try:
#         with open(filepath, 'rb') as file:
#             # Create a Django File object
#             django_file = File(file)

#             return django_file

#     except FileNotFoundError:
#         raise FileNotFoundError("File not found.")
#     except IOError:
#         raise IOError("Error occurred while reading the file.")
#     except Exception as e:
#         raise Exception(f"Error creating Django File object: {str(e)}")


def create_django_file(filepath):
    """
    Creates a Django File object from the given filepath.

    Args:
        filepath (str): The path to the file.

    Returns:
        object: The created Django File object.

    Raises:
        FileNotFoundError: If the file is not found.
        IOError: If an error occurs while reading the file.
        FileObjectCreationError: If an error occurs during the process of creating the Django File object.
    """
    try:
        file = open(filepath, 'rb')
        django_file = File(file)
        django_file.seek(0)  # Reset the file pointer to the beginning
        return django_file

    except FileNotFoundError:
        raise FileNotFoundError("File not found.")
    except IOError:
        raise IOError("Error occurred while reading the file.")
    except Exception as e:
        raise Exception(f"Error creating Django File object: {str(e)}")



def convert_field_type(data, field, type):
    """This function takes in a data set, field name and type as parameters 
    and converts the field to the specified type."""
    # Convert the field to the specified type
    data[field] = type(data[field])
    # Return the modified data set
    return data


def generate_response(status, message, data=None, pagination_data=None):
    response_data = {"status": status, "message": message}
    if data is not None:
        response_data["data"] = data
    if pagination_data is not None:
        response_data["count"] = pagination_data
    return Response(response_data, status=status)

def generate_error_response(status=None, errors=None):
    response_data = {"status": status, "errors": errors}
    return Response(response_data, status=status)


def serialize_errors(serializer):
    errors = {}
    for field, error_msgs in serializer.errors.items():
        if isinstance(error_msgs, list):
            errors[field] = error_msgs[0]  # use the first error message
        else:
            errors[field] = error_msgs
    return {
        "error": {
            "code": 400,
            "message": errors
        }
    }


class CustomJSONEncoder(json.JSONEncoder):
    """CustomJSONEncoder class to encode objects into JSON"""
    # Override default method to convert ObjectId, datetime, FieldFile and UUID objects into strings

    def default(self, obj):
        # if isinstance(obj, ObjectId):
        #     return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            # Convert datetime to string
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, FieldFile):
            return obj.url  # Return the URL of the FieldFile object
        elif isinstance(obj, UUID):
            return str(obj)  # Convert UUID to string
        return json.JSONEncoder.default(self, obj)  # Default


class ListQuerySerializer(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)





def validate_regex(value, pattern):
    """Validate if a value matches a regex pattern."""
    return bool(re.match(pattern, value))




def replace_placeholder_with_id_function(model, attribute, placeholder_key, data,id_key):
    """
    A function to replace a placeholder value in request.data with the corresponding model's ID.

    Args:
        model (class): The Django model class to query.
        attribute (str): The attribute name in the model to match.
        placeholder_key (str): The key in request.data where the placeholder value is located.
        request (HttpRequest): The Django HttpRequest object.

    Example:
        replace_placeholder_with_id_function(Endpoint, 'name', 'endpoint_name', request)
    """
    if data.get(placeholder_key) is not None:
        # Get the placeholder value from data
        placeholder_value = data[placeholder_key]
        obj = model.objects.filter(**{attribute: placeholder_value}).first()
        if obj:
            # Replace the placeholder value with the object's ID
            data[id_key] = obj.id
        return data
# Usage example in a view function:
# Call the function to replace the placeholder in your view function
# replace_placeholder_with_id_function(Endpoint, 'name', 'endpoint_name', request)
