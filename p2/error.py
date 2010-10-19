"""class WrapErr():
    # Lex errors
    UNKNOWN_CHAR = 0
    INT_OVERFLOW = 1
    UNCLOSED_COM = 2
"""
class Error(Exception):
    nline = 0
    ncol = 0

    def __init__(self, nline, ncol):
        pass

    def printError(self, err)

class LexicalError(Error):
    UNKNOWN_CHAR = 0
    INT_OVERFLOW = 1
    UNCLOSED_COM = 2
    
    _errStrings = ("Invalid character",
                   "Integer overflow",
                   "Unclosed comment")

    def __init__(self, err, nline, ncol):
        self.err = err
        self.nline = nline
        self.ncol = ncol
        #self._printError()

    def _printError(self):
        print "\n[LEX ERROR] ", self._errStrings[self.err],


class SyntacticalError(Error):
    UNEXPECTED_SYM = 0

    _errStrings = ("Unexpected symbol")

    def __init__
