class MUEError(Exception):
    pass

class NoMatchFound(MUEError):
    message = 'no match found'
class InvalidPick(MUEError):
    message = 'input not understood'
class ExclusiveRecent(MUEError):
    message = 'template is set by --recent flag'
class FileNotFound(MUEError):
    message = 'unable to find specified input file'
class NoFiles(MUEError):
    message = 'no markdown files were given'
class SubprocessFailed(MUEError):
    message = 'subprocess returned with non-zero exit code. run with -d to debug'

