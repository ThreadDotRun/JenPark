import logging

class CrmErrorHandler:
    """Centralizes error handling and logging for the CRM."""
    
    def __init__(self):
        logging.basicConfig(filename='crm_errors.log', level=logging.ERROR,
                           format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_error(self, exception, context):
        """Handle and log errors, returning a standardized error response."""
        error_message = f"{context}: {str(exception)}"
        logging.error(error_message)
        return {
            "status": "error",
            "message": error_message
        }