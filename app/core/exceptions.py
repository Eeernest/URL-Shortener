class AppBaseException(Exception):
  status_code = 500
  detail = "An error occured"

class ShortCodeGenerationError(AppBaseException):
  # raised when a unique short codecannot be generated
  
  detail = "Failed to generate unique code"

class UrlNotFoundError(AppBaseException):
  # raised when a short code does not exist in cache and db
  
  status_code = 404
  detail = "Short URL not found"