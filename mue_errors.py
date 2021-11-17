class MUEError(Exception):
    pass
class NoMatchFound(MUEError):
    message = 'no match found'
class SubprocessFailed:
    message = 'execution failed'

