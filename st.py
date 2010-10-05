class ST:
    """Clase para la gestion de la tabla de simbolos"""
    _table = None

    def __init__(self):
        self._table = {}
        self._index = 1
        # Insertamos las palabras reservadas
        self._table["and"] = [True]
        self._table["array"] = [True]
        self._table["begin"] = [True]
        self._table["const"] = [True]
        self._table["div"] = [True]
        self._table["do"] = [True]
        self._table["else"] = [True]
        self._table["end"] = [True]
        self._table["if"] = [True]
        self._table["mod"] = [True]
        self._table["not"] = [True]
        self._table["of"] = [True]
        self._table["or"] = [True]
        self._table["procedure"] = [True]
        self._table["program"] = [True]
        self._table["record"] = [True]
        self._table["then"] = [True]
        self._table["type"] = [True]
        self._table["var"] = [True]
        self._table["while"] = [True]
        # Insertamos los identificadores estandar
        self.insertST("integer")
        self.insertST("boolean")
        self.insertST("false")
        self.insertST("true")
        self.insertST("read")
        self.insertST("write")

    def insertST(self, lex, reserved = False, line = None, pos = None):
        atributes = [reserved, self._index]
        if line:
            atributes.append(line, pos)
        self._table[lex] = atributes
        self._index += 1

    def isST(self, lex):
        return self._table.has_key(lex)

    def isReserved(self, lex):
        try:
            r = self._table[lex][0]
            return r
        except KeyError:
            return None

    def getIndex(self, lex):
        try:
            i = self._table[lex][1]
            return i
        except KeyError:
            return None
        except IndexError:
            return None

    def getLine(self, lex):
        try:
            l = self._table[lex][2]
            return l
        except KeyError:
            return None
        except IndexError:
            return None

    def getPos(self, lex):
        try:
            c = self._table[lex][3]
            return c
        except KeyError:
            return None
        except IndexError:
            return None

    def printST(self):
        for i in self._table:
            print i + "\t\t",
            for j in self._table[i]:
                print j, "\t",
            print ""
