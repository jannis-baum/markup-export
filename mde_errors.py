class MDEError(Exception):
    pass
class NoMatchFound(MDEError):
    message = 'no match found'