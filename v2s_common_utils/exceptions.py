from rest_framework.exceptions import APIException

class CustomValidationException(APIException):
    """Custom exception class for formatting error messages."""
    def __init__(self, error_list):
        self.error_list = error_list
        super().__init__(detail=self.error_list)

class CustomValidationError:
    """Helper class for creating validation error dictionaries."""
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def as_dict(self):
        return {"error_code": self.error_code, "error_message": self.error_message}
    
    
