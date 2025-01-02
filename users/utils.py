from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
import re


def custom_exception_handler(exc, context):
    # Get the standard response
    response = exception_handler(exc, context)
    
    if response is not None:
        # Handle ValidationError explicitly for meaningful details
        if isinstance(exc, ValidationError):
            response.data = {
                "success": False,
                "error": {
                    "code": response.status_code,  # HTTP status code
                    "message": "Validation failed.",
                    "details": response.data,  # Include detailed validation errors
                },
            }
        else:
            response.data = {
                "success": False,
                "error": {
                    "code": response.status_code,
                    "message": str(exc),  # More generic error message
                    "details": response.data,  # Include raw response details for debugging
                },
            }
            
    return response
