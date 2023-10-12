from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from functools import wraps
from traceback import print_exc

from v2s_common_utils.message import STATUS_MESSAGES
from v2s_common_utils.utils import generate_response,generate_error_response
from v2s_common_utils.exceptions import CustomValidationException


# def validate_object_id(pk, id_name):
#     if not ObjectId.is_valid(pk):
#         return generate_response(status=status.HTTP_400_BAD_REQUEST, message=f'Invalid {id_name} ID.')
#     return None


def handle_exception(exception):
    """
    A helper function to handle different types of exceptions and return an appropriate response.

    Args:
        exception: An exception object that needs to be handled.

    Returns:
        A Response object with an appropriate error message and status code.
    """
    if isinstance(exception, ValidationError) or isinstance(exception, NotFound):
        message = exception.detail
        return generate_response(status=status.HTTP_400_BAD_REQUEST, message=message)
    if isinstance(exception, CustomValidationException):
        errors = exception.error_list
        return generate_error_response(status=status.HTTP_200_OK, errors=errors)
    elif isinstance(exception, FileNotFoundError) or isinstance(exception, ValueError):
    # elif isinstance(exception, CustomException) or isinstance(exception, FileNotFoundError) or isinstance(exception, ValueError):
        message = str(exception)
        return generate_response(status=status.HTTP_400_BAD_REQUEST, message=message)
    elif isinstance(exception, CustomException):
        # Handle CustomException by extracting the error code and message
        error_response = {
            "error_code": exception.error_code,
            "error_message": exception.error_message
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # Set appropriate HTTP status code

    else:
        print_exc()
        message = STATUS_MESSAGES.get(500)
        return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message)


def check_required_keys(keys):
    """
    A decorator that checks if the specified keys are present in the request query parameters or request data and not None.
    """

    def decorator(view_func):
        @ wraps(view_func)
        def wrapper(*args, **kwargs):
            request = args[1]
            if request.method == 'GET':
                data = request.query_params
            elif request.method in ['POST', 'PUT']:
                data = request.data
            else:
                return generate_response(status=status.HTTP_400_BAD_REQUEST, message='Invalid request method')

            for key in keys:
                if key not in data or data[key] is None:
                    return generate_response(status=status.HTTP_400_BAD_REQUEST, message=f"'{key}' is required and cannot be None.")

            return view_func(*args, **kwargs)
        return wrapper
    return decorator


# def validate_ids(ids_dict):
#     """
#     A decorator that validates multiple object IDs in the request URL.

#     Args:
#         id_dict (dict): A dictionary that maps ID names to display names.

#     Returns:
#         A function that takes a view function as an argument and returns a new function
#         that performs the validation on each ID and calls the view function if all IDs
#         are valid. If any ID is invalid, the decorator returns a 400 Bad Request response
#         with an error message.

#     Example usage:
#         @validate_ids({'contract_id': 'Contract ID', 'template_id': 'Template ID'})
#         def my_view(request, contract_id, template_id):
#             # Do something with the validated IDs.
#             pass
#     """
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             for id, display_name in ids_dict.items():
#                 pk = kwargs.get(f'{id}')
#                 if not ObjectId.is_valid(pk):
#                     return generate_response(status=status.HTTP_400_BAD_REQUEST, message=f'Invalid {display_name}: {pk}')
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator


# # def validate_tenet_id(model, lookup_field='pk'):
#     """
#     A decorator that checks if the authenticated user has the same tenant ID as the object being accessed.

#     Args:
#         model (Model): The model of the object being accessed.
#         lookup_field (str, optional): The name of the lookup field to use. Defaults to 'pk'.

#     Returns:
#         function: The decorated function.
#     """
#     def decorator(view_func):
#         @ wraps(view_func)
#         def wrapped_view(self, request, *args, **kwargs):
#             lookup_field_value = kwargs.get(
#                 lookup_field) or request.data.get(lookup_field)
#             if not lookup_field_value:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=f'Invalid lookup field value. Please provide a valid {lookup_field}.')

#             try:
#                 if lookup_field == 'pk' or lookup_field in request.data or lookup_field in kwargs:
#                     obj = model.objects.get(pk=ObjectId(lookup_field_value))
#                 else:
#                     obj = model.objects.get(
#                         **{lookup_field: lookup_field_value})

#             except model.DoesNotExist:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=STATUS_MESSAGES.get(404).format(model.__name__, lookup_field_value))

#             if not request.user.is_superuser and obj.tenet_id != self.request.user.tenet_id:
#                 return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(403))

#             return view_func(self, request, *args, **kwargs)

#         return wrapped_view

#     return decorator


# def validate_tenet_id_by_kwargs(model, lookup_field=None):
#     """
#     A decorator that checks if the authenticated user has the same tenant ID as the object being accessed.

#     Args:
#         model (Model): The model of the object being accessed.
#         lookup_field (str, optional): The name of the lookup field to use. Defaults to 'pk'.

#     Returns:
#         function: The decorated function.
#     """
#     def decorator(view_func):
#         @ wraps(view_func)
#         def wrapped_view(self, request, *args, **kwargs):
#             lookup_field_value = kwargs.get(
#                 lookup_field)
#             if not lookup_field_value:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=f'Invalid lookup field value. Please provide a valid {lookup_field}.')
#             try:
#                 obj = model.objects.get(
#                     **{lookup_field: lookup_field_value})
#             except model.DoesNotExist:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=STATUS_MESSAGES.get(404).format(model.__name__, lookup_field_value))

#             if not request.user.is_superuser and obj.tenet_id != self.request.user.tenet_id:
#                 return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(403))

#             return view_func(self, request, *args, **kwargs)

#         return wrapped_view

#     return decorator


# def validate_tenant_id_by_lookup(model1, model2, fk_field):
#     """
#     A decorator that validates the tenant ID of a model by looking up a related model through a foreign key field.

#     Args:
#         model1 (Model): The first model to be looked up.
#         model2 (Model): The related model to be looked up through `fk_field` in `model1`.
#         fk_field (str): The name of the foreign key field in `model1` that links to `model2`.

#     Returns:
#         A decorated function that checks the tenant ID of `model2` and returns an HTTP response with an error message if the tenant ID does not match the authenticated user's tenant ID.

#     Raises:
#         None.
#     """

#     def decorator(view_func):
#         @ wraps(view_func)
#         def wrapped_view(self, request, pk, *args, **kwargs):
#             try:
#                 instance1 = model1.objects.get(pk=ObjectId(pk))
#             except model1.DoesNotExist:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=STATUS_MESSAGES.get(404).format(model1.__name__, pk))

#             try:
#                 instance2_id = getattr(instance1, fk_field)
#                 instance2 = model2.objects.get(pk=ObjectId(instance2_id))
#             except model2.DoesNotExist:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=STATUS_MESSAGES.get(404).format(model2.__name__, instance2_id))

#             if instance2.tenet_id != self.request.user.tenet_id:
#                 return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(403))

#             return view_func(self, request, pk, *args, **kwargs)

#         return wrapped_view

#     return decorator


# def validate_contract_owner_or_reviewer(view_func):
#     """
#     Decorator that validates that the request user is authorized to access a resource associated with a contract.

#     The decorator checks that the request user is either the contract owner or a reviewer associated with the contract.

#     Args:
#         view_func (callable): The view function to decorate.

#     Returns:
#         callable: The decorated view function.
#     """
#     @ wraps(view_func)
#     def wrapped_view(self, request, *args, **kwargs):
#         user_id = str(self.request.user._id)
#         pk = kwargs.get('contract_id') or kwargs.get(
#             'pk') or self.request.data.get('contract_id')
#         if pk:
#             contract = Contracts.objects.filter(
#                 pk=ObjectId(pk)).first()
#             if not contract:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message='Contract not found.')
#             if not (contract.contract_owner_user_id == user_id or
#                     Reviewers.objects.filter(reviewer_user_id=user_id, contract_id=pk).exists()):
#                 return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(403))
#         return view_func(self, request, *args, **kwargs)

#     return wrapped_view


# def validate_reviewer(view_func):
#     """
#     A decorator that checks whether the requesting user is authorized to access the resource.
#     The requesting user must be associated with the contract by being either the contract owner or a reviewer.
#     """

#     def wrapper_func(self, request, *args, **kwargs):
#         user_id = str(self.request.user._id)
#         pk = kwargs.get('contract_id') or kwargs.get(
#             'pk') or self.request.data.get('contract_id')
#         reviewer_user_ids = ReviewerService.get_reviewer_user_ids_by_contract_id(
#             pk)
#         if user_id in reviewer_user_ids:
#             return view_func(self, request, *args, **kwargs)
#         else:
#             return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(403))
#     return wrapper_func


# def validate_user_id(model, user_field):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, request, *args, **kwargs):
#             # Assuming the object ID is passed as a keyword argument
#             obj_id = kwargs.get('pk')
#             try:
#                 obj = model.objects.get(id=obj_id)
#                 if request.user._id != getattr(obj, user_field)._id:
#                     return generate_response(status=status.HTTP_403_FORBIDDEN, message=STATUS_MESSAGES.get(401))
#             except model.DoesNotExist:
#                 return generate_response(status=status.HTTP_404_NOT_FOUND, message=f'{model.__name__} not found with id {obj_id}.')

#             return func(self, request, *args, **kwargs)
#         return wrapper
#     return decorator


# def set_tenet_id_in_request_data(func):
#     """
#     A decorator that sets the authenticated user's tenant ID in the `request.data` dictionary.

#     Args:
#         func (callable): The function to be decorated.

#     Returns:
#         A decorated function that sets the `tenet_id` key in the `request.data` dictionary to the authenticated user's tenant ID and returns the result of calling the original function.

#     Raises:
#         None.
#     """
#     def wrapper(*args, **kwargs):
#         request = args[1]
#         request.data['tenet_id'] = request.user.tenet_id
#         return func(*args, **kwargs)
#     return wrapper


# def set_user_in_request_data(func):
#     @wraps(func)
#     def wrapper(self, request, *args, **kwargs):
#         if request.user.is_anonymous:
#             return generate_response(status=status.HTTP_404_NOT_FOUND, message=STATUS_MESSAGES.get(403).format('User', request.user._id))
#         request.data['user'] = request.user._id
#         return func(self, request, *args, **kwargs)
#     return wrapper


# class CustomException(Exception):
#     def __init__(self, message):
#         self.message = message
#         super().__init__(message)


class FileObjectCreationError(Exception):
    pass


class CustomException(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)