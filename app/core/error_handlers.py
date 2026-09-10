from flask import request

from app.core.errors import AppError
from app.core.responses import error_response


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        if request.path.startswith("/api/"):
            return error_response(
                message=error.message,
                errors=error.errors,
                status_code=error.status_code
            )
        
        return (
            f"{error.status_code} - {error.message}", error.status_code
        )
    
    @app.errorhandler(404)
    def handle_not_found(error):

        if request.path.startswith("/api/"):
            return error_response(
                message="Response not Found", status_code=404
            )
        
        return "404 - page not found", 404

    @app.errorhandler(500)
    def handle_server_error(error):

        if request.path.startswith("/api/"):
            return error_response(
                message="An internal server error occured...", status_code=500
            )
        
        return "500 Internal server error occured.", 500
    

    
