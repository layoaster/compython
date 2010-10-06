class WrapErr():
    # Lex errors
    UNKNOWN_CHAR = 0
    INT_OVERFLOW = 1
    UNCLOSED_COM = 2

class Error(Exception):
    def __init__(self):
        pass

class LexicalError(Error):
    _errStrings = ("Caracter no reconocido",
                  "Desbordamiento de entero",
                  "Comentario sin cerrar")

    def __init__(self, err, nline, ncol):
        self.err = err
        self.nline = nline
        self.ncol = ncol
        #self._printError()

    def _printError(self):
        print self.nline, ":", self.ncol, "[LEX ERROR] ", self._errStrings[self.err]
