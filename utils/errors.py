class AppError(Exception):
    """Base class for application errors"""
    pass

class AuthError(AppError):
    """Authentication errors"""
    pass

class ValidationError(AppError):
    """Validation errors"""
    pass

class ToolExecutionError(Exception):
    """Errors during tool execution"""
    pass 