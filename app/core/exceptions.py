class ShortCodeGenerationError(Exception):
  # raised when a unique short codecannot be generated
  pass

class UrlNotFoundError(Exception):
  # raised when a short code does not exist in cache and db
  pass