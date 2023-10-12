#Python Imports
import re

#Django Imports
from django.contrib.auth import authenticate

#Third-Party Imports

#Project-Specific Imports

#Relative Import



class FieldValidationException(Exception):
    """
    Custom exception for field validation errors.

    Args:
        error_code (str): Error code associated with the validation error.
        error_message (str): Error message describing the validation error.

    Attributes:
        error_code (str): Error code associated with the validation error.
        error_message (str): Error message describing the validation error.

    Methods:
        to_dict(): Converts the exception to a dictionary.

    Example:
        raise FieldValidationException("E0600", "Permission name cannot be blank.")
    """

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def to_dict(self):
        """Converts the exception to a dictionary."""
        return {
            "error_code": self.error_code,
            "error_message": self.error_message
        }
        

class ValidatorBase:
    """
    Base class for field validation.

    Args:
        field_name (str): The name of the field being validated.

    Attributes:
        field_name (str): The name of the field being validated.
        errors (list): List to store validation errors.

    Methods:
        add_error(error_code, error_message): Adds a validation error to the list.
        validate(value): Validates the field's value (must be implemented by subclasses).

    Example:
        class MyValidator(ValidatorBase):
            def validate(self, value):
                if not value:
                    self.add_error("E001", "Field cannot be empty.")
    """

    def __init__(self, field_name):
        self.field_name = field_name
        self.errors = []

    def add_error(self, error_code, error_message):
        """Adds a validation error to the list."""
        self.errors.append(FieldValidationException(error_code, error_message).to_dict())

    def validate(self, value):
        """Validates the field's value (must be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method")



class MinMaxLengthValidator(ValidatorBase):
    def __init__(self, field_name, min_length=None, max_length=None, error_code=None, error_message=None):
        super().__init__(field_name)
        self.min_length = min_length
        self.max_length = max_length
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        if self.min_length is not None and len(value) < self.min_length:
            self.add_error(self.error_code, self.error_message)
        if self.max_length is not None and len(value) > self.max_length:
            self.add_error(self.error_code, self.error_message)

class EmptyValidator(ValidatorBase):
    """
    Validator for checking if a field is empty or not based on 'allow_blank' parameter.

    Args:
        field_name (str): The name of the field being validated.
        allow_blank (bool, optional): If True, the field is allowed to be empty. Default is False.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate that 'my_field' is not empty
        EmptyValidator('my_field', error_code="E001", error_message="Field cannot be empty.")
    """

    def __init__(self, field_name, allow_blank=False, error_code=None, error_message=None):
        super().__init__(field_name)
        self.allow_blank = allow_blank
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if the field is empty or not."""
        if not self.allow_blank and not value:
            self.add_error(self.error_code, self.error_message)


class AlphanumericValidator(ValidatorBase):
    """
    Validator for checking if a field contains only alphanumeric characters.

    Args:
        field_name (str): The name of the field being validated.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate that 'my_field' contains only alphanumeric characters
        AlphanumericValidator('my_field', error_code="E002", error_message="Field must be alphanumeric.")
    """

    def __init__(self, field_name, error_code=None, error_message=None):
        super().__init__(field_name)
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if the field contains only alphanumeric characters."""
        # Check if the value matches the regex pattern for alphanumeric characters only
        regex_pattern = r'^[A-Za-z0-9]+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)
class AlphanumericWithWhitespaceValidator(ValidatorBase):
    """
    Validator for checking if a field contains only alphanumeric characters and whitespace.

    Args:
        field_name (str): The name of the field being validated.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate that 'my_field' contains only alphanumeric characters and whitespace
        AlphanumericWithWhitespaceValidator('my_field', error_code="E003", error_message="Field must be alphanumeric with whitespace.")
    """

    def __init__(self, field_name, error_code=None, error_message=None):
        super().__init__(field_name)
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if the field contains only word characters and whitespace characters."""
        regex_pattern = r'^[\w\s]+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)


class DigitsOnlyValidator(ValidatorBase):
    """
    Validator for checking if a field contains only digits.

    Args:
        field_name (str): The name of the field being validated.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate that 'my_field' contains only digits
        DigitsOnlyValidator('my_field', error_code="E004", error_message="Field must contain digits only.")
    """

    def __init__(self, field_name, error_code=None, error_message=None):
        super().__init__(field_name)
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if the field contains digits only."""
        regex_pattern = r'^\d+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

class RegexValidator(ValidatorBase):
    """
    Validator for applying custom regular expression-based validation methods to a field.

    Args:
        field_name (str): The name of the field being validated.
        regex_pattern (str, optional): The regular expression pattern for validation.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.
        validation_method (str, optional): The name of the custom validation method to apply.

    Example:
        # Validate 'phone_number' field using a custom validation method 'validate_mobile_number'
        RegexValidator('phone_number', regex_pattern=r'^\+\d{1,3}\s?\(\d{1,4}\)\s?\d{6,}$',
                       error_code="E001", error_message="Invalid phone number format",
                       validation_method="validate_mobile_number")
    """

    def __init__(self, field_name, regex_pattern=None, error_code=None, error_message=None, validation_method=None):
        super().__init__(field_name)
        self.regex_pattern = regex_pattern
        self.error_code = error_code
        self.error_message = error_message
        self.validation_method = validation_method

    def validate(self, value):
        """Validates the field using the specified custom validation method."""
        if self.validation_method:
            getattr(self, self.validation_method)(value)

    def validate_mobile_number(self, value):
        """Validates a mobile number using a standard regex pattern."""
        regex_pattern = r'^\+\d{1,3}\s?\(\d{1,4}\)\s?\d{6,}$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_email(self, value):
        """Validates an email address using a standard regex pattern."""
        regex_pattern = r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_allow_specific_special_characters(self, value):
        """Validates if the value contains only word characters, '.', ',', and whitespace."""
        regex_pattern = r'^[\w\s.,]+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_digits_only(self, value):
        """Validates if the value contains digits only."""
        regex_pattern = r'^\d+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

class ModelAttributeExistsValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value exists in the database.

    Args:
        field_name (str): The name of the field being validated.
        model_class (class): The model class in which to check for the existing attribute value.
        attribute_name (str): The name of the attribute to check for duplicates.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate 'email' field to ensure it exists in the 'User' model
        ModelAttributeExistsValidator('email', User, 'email', error_code="E001", error_message="Email already exists")
    """

    def __init__(self, field_name, model_class, attribute_name, error_code=None, error_message=None):
        super().__init__(attribute_name)
        self.field_name = field_name
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if a record with the same attribute value already exists in the database."""
        filter_kwargs = {self.attribute_name: value}
        existing_record = self.model_class.objects.filter(**filter_kwargs).first()
        if existing_record:
            self.add_error(self.error_code, self.error_message)        
            
class AuthPassValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value exists in the database.

    Args:
        model_class (class): The model class in which to check for the existing attribute value.
        attribute_name (str): The name of the attribute to check for duplicates.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.
        **kwargs: Additional keyword arguments for record validation.

    Example:
        # Validate 'email' field to ensure it exists in the 'User' model
        AuthPassValidator(User, 'email', error_code="E001", error_message="Email already exists", username="user123")
    """

    def __init__(self, model_class, attribute_name, error_code=None, error_message=None, **kwargs):
        super().__init__(attribute_name)
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message
        self.kwargs = kwargs

    def validate(self):
        """Validates if a record with the same attribute value already exists in the database."""
        existing_record = authenticate(**self.kwargs)
        if not existing_record:
            self.add_error(self.error_code, self.error_message)



class ModelAttributeNotExistsValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value does not exist in the database.

    Args:
        field_name (str): The name of the field being validated.
        model_class (class): The model class in which to check for the absence of the attribute value.
        attribute_name (str): The name of the attribute to check for non-existence.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate 'username' field to ensure it doesn't exist in the 'User' model
        ModelAttributeNotExistsValidator('username', User, 'username', error_code="E002", error_message="Username already exists")
    """

    def __init__(self, field_name, model_class, attribute_name, error_code=None, error_message=None):
        super().__init__(attribute_name)
        self.field_name = field_name
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if a record with the same attribute value does not exist in the database."""
        filter_kwargs = {self.attribute_name: value}
        existing_record = self.model_class.objects.filter(**filter_kwargs).first()
        if not existing_record:
            self.add_error(self.error_code, self.error_message)


class FieldRelatedValidator(ValidatorBase):
    """
    Validator for checking if a related field value exists in the database.

    Args:
        field_name (str): The name of the field being validated.
        model_class (class): The model class to search for related objects.
        lookup_field (str): The name of the field to use for lookup in related objects.
        error_code (str, optional): The error code for validation failures.
        error_message (str, optional): The error message for validation failures.

    Example:
        # Validate 'user_id' field to ensure it's a valid User ID in the 'User' model
        FieldRelatedValidator('user_id', User, 'id', error_code="E003", error_message="User does not exist")
    """

    def __init__(self, field_name, model_class, lookup_field_alias, error_code=None, error_message=None):
        super().__init__(field_name)
        self.model_class = model_class
        self.lookup_field_alias = lookup_field_alias
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if the related field value exists in the database."""
        if value:
            filter_kwargs = {self.lookup_field_alias: value}
            existing_object = self.model_class.objects.filter(**filter_kwargs).first()
            if existing_object:
                self.add_error(self.error_code, self.error_message)



class ValidatorHelper:
    """
    Helper class for validating data using a list of validators and converting error sets to lists.

    Attributes:
        None

    Methods:
        validate_and_collect_errors(data, validators):
            Validate data using a list of validators and collect unique errors.

        convert_errors_set_to_list(errors_set):
            Convert a set of errors (error code, error message) to a list of dictionaries.

    Example:
        # Create a list of validators and validate data
        validators = [MinMaxLengthValidator('field1', min_length=1, max_length=100, error_code="E001", error_message="Field1 error")]
        data = {'field1': ''}
        errors_set = ValidatorHelper.validate_and_collect_errors(data, validators)
        
        # Convert the errors set to a list of dictionaries
        errors_list = ValidatorHelper.convert_errors_set_to_list(errors_set)
    """

    @staticmethod
    def validate_and_collect_errors(data, validators):
        """
        Validate data using a list of validators and collect unique errors.

        Args:
            data (dict): The data to be validated.
            validators (list): A list of validator objects.

        Returns:
            set: A set containing unique errors as (error code, error message) tuples.

        Example:
            # Create a list of validators and validate data
            validators = [MinMaxLengthValidator('field1', min_length=1, max_length=100, error_code="E001", error_message="Field1 error")]
            data = {'field1': ''}
            errors_set = ValidatorHelper.validate_and_collect_errors(data, validators)
        """
        errors_set = set()

        for validator in validators:
            value = data.get(validator.field_name)
            validator.validate(value)
            errors_set.update((error['error_code'], error['error_message']) for error in validator.errors)

        return errors_set

    @staticmethod
    def convert_errors_set_to_list(errors_set):
        """
        Convert a set of errors (error code, error message) to a list of dictionaries.

        Args:
            errors_set (set): A set of unique errors as (error code, error message) tuples.

        Returns:
            list: A list of dictionaries with 'error_code' and 'error_message' keys.

        Example:
            # Convert the errors set to a list of dictionaries
            errors_list = ValidatorHelper.convert_errors_set_to_list(errors_set)
        """
        return list(map(lambda x: {'error_code': x[0], 'error_message': x[1]}, errors_set))
