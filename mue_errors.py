class MUEError(Exception):
    pass

class NoMatchFound(MUEError):
    message = 'no match found'
class SubprocessFailed(MUEError):
    message = 'execution failed'
class InvalidPick(MUEError):
    message = 'input not understood'
class ExclusiveRecent(MUEError):
    message = 'template is set by --recent flag'

