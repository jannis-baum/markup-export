class MUEError(Exception):
    pass

class NoMatchFound(MUEError):
    message = 'no match found'
class SubprocessFailed(MUEError):
    message = 'execution failed'
class InvalidPick(MUEError):
    message = 'input not understood'
class FileNotFound(MUEError):
    message = 'unable to find specified input file'
class SubprocessFailed(MUEError):
    message = 'subprocess returned with non-zero exit code. run with -d to debug'

