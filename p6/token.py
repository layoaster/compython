#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase que envuelve la representacion interna de los tokens y la propia clase token (con el par componente lexico, valor (identificadores y numerales)).
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapTk:

    ASTERISK          = 1
    ENDTEXT           = 2
    LEFTPARENTHESIS   = 3
    LETTER            = 4
    RIGHTPARENTHESIS  = 5
    TOKEN_ERROR       = 6
    VERTICALBAR       = 7

    TokStrings = ("ASTERISK", "ENDTEXT", "LEFTPARENTHESIS", "LETTER",
                  "RIGHTPARENTHESIS", "TOKEN_ERROR", "VERTICALBAR")

    TokLexemes = ("*", "$", "(", "letter", ")", "", "|")

    @classmethod
    def toStr(self, token):
        return "_" + str(token)

    @classmethod
    def toToken(self, string):
        token = string[1:]
        return int(token)

class Token:

    def __init__(self, token, value=None):
        """ Constructor de la clase
            _token = token que representa
            _value = lexema o numero para los tokens ID y NUMERAL, para ID este valor hacer de apuntador en la tabla de simbolos
        """
        self._token = token
        self._value = value

    def setToken(self, token):
        """ Setter del numero que representa internamente al token
        """
        self._token = token

    def setValue(self, value):
        """ Setter del valor que puede tomar el token en caso de ser del tipo ID o NUMERAL
        """
        self._value = value

    def getToken(self):
        """ Getter del numero que representa internamente al token
        """
        return self._token

    def getValue(self):
        """ Setter del valor que puede tomar el token en caso de ser del tipo ID o NUMERAL
        """
        return self._value

    def getLexeme(self):
        """ Devuelve cadena que da nombre al TOKEN, en el caso de los token ID y NUMERAL devuelve su valor
            util en el informe del error, cuando se muestran el token encontrado
        """
        if self._token in (WrapTk.ID, WrapTk.NUMERAL):
            return str(self._value)
        else:
            return WrapTk.TokLexemes[self._token - 1]

    def getTokLexeme(self):
        """ Devuelve cadena que da nombre al TOKEN, en el caso de los token ID y NUMERAL no devuelve su valor
            util en el informe del error, cuando se muestran los token esperados
        """
        return WrapTk.TokLexemes[self._token - 1]

    def __eq__(self, token):
        """ Sobrecarga del operador de comparacion "igual que", para establecer las comparaciones con un enteros
            tambien es necesario para insertar el objeto en un set/frozenset
        """
        if self._token == token:
            return True
        else:
            return False

    def __hash__ (self):
        """ Sobrecarga de la funcion hash (identificando el objeto token de manera unica) necesaria para insertar
            el objeto en un set/frozenset
        """
        return self._token
