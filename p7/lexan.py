#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Modulo del Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string
import re
from error import LexError
from st import SymbolTable, st
from token import WrapTk, Token

class LexAn:

    _patterns = [
        (WrapTk.COMMENT,         r"\(\*|\{|//"),
        (WrapTk.ASTERISK,        r"\*"),
        (WrapTk.BECOMES,         r":="),
        (WrapTk.COLON,           r":"),
        (WrapTk.COMMA,           r","),
        (WrapTk.DOUBLEDOT,       r"\.\."),
        (WrapTk.EQUAL,           r"="),
        (WrapTk.NOTEQUAL,        r"\<\>"),
        (WrapTk.NOTGREATER,      r"\<="),
        (WrapTk.NOTLESS,         r"\>="),
        (WrapTk.GREATER,         r"\>"),
        (WrapTk.ID,              r"[a-zA-Z]\w*"),
        (WrapTk.LEFTBRACKET,     r"\["),
        (WrapTk.LEFTPARENTHESIS, r"\("),
        (WrapTk.LESS,            r"\<"),
        (WrapTk.MINUS,           r"-"),
        (WrapTk.NUMERAL,         r"\d+"),
        (WrapTk.PERIOD,          r"\."),
        (WrapTk.PLUS,            r"\+"),
        (WrapTk.RIGHTBRACKET,    r"\]"),
        (WrapTk.RIGHTPARENTHESIS,r"\)"),
        (WrapTk.SEMICOLON,       r";")
    ]

    _reserved = { 
        "and"       : WrapTk.AND,
        "array"     : WrapTk.ARRAY,
        "begin"     : WrapTk.BEGIN,
        "const"     : WrapTk.CONST,
        "div"       : WrapTk.DIV,
        "do"        : WrapTk.DO,
        "else"      : WrapTk.ELSE,
        "end"       : WrapTk.END,
        "if"        : WrapTk.IF,
        "mod"       : WrapTk.MOD,
        "not"       : WrapTk.NOT,
        "of"        : WrapTk.OF,
        "or"        : WrapTk.OR,
        "procedure" : WrapTk.PROCEDURE,
        "program"   : WrapTk.PROGRAM,
        "record"    : WrapTk.RECORD,
        "then"      : WrapTk.THEN,
        "type"      : WrapTk.TYPE,
        "var"       : WrapTk.VAR,
        "while"     : WrapTk.WHILE
    }

    def __init__(self):
        """ Constructor de la clase
        """
        self._nline = 0
        self._ncol = 1
        self._tokstart = 1
        self._buffer = ""
        self._fin = None
        self._flags = re.UNICODE | re.IGNORECASE

        parts = []
        for name, rule in self._patterns:
            parts.append("(?P<%s>%s)" % (WrapTk.toStr(name), rule))

        self._regex = re.compile("|".join(parts), self._flags)
        self._wsregex = re.compile("\s*", re.MULTILINE)

    def openFile(self, fin):
        try:
            self._fin = open(fin, "rU")
        except IOError:
            raise

    def _readLine(self):
        """ Lee una linea del fichero y la inserta en el buffer, ignorando lineas en blanco
        """
        while self._buffer == "":
            self._buffer = self._fin.readline()
            if self._buffer == "": # EOF
                return False
            self._nline += 1
            self._ncol = 1
            self._buffer = self._buffer.rstrip()

        # Ignorar espacios en blanco
        wsmatch = self._wsregex.match(self._buffer)
        if wsmatch:
            self._buffer = self._buffer[wsmatch.end():]
            self._ncol += wsmatch.end()
            self._tokstart = self._ncol
        return True

    def _ignComment(self):
        """ Procesado de comentarios, incluyendo comentarios anidados, multilinea y malformados (sin cerrar)
        """
        comment = re.compile("(?P<leftbracket>\{)|(?P<leftparenthesis>\(\*)|(?P<rightbracket>\})|(?P<rightparenthesis>\*\))|(?P<doublebar>//)")
        match = comment.search(self._buffer)
        if match.lastgroup != "doublebar":
            nbra = 1
            npar = 1
            flag = True
            while (nbra != 0 or npar != 0):
                if flag:
                    nbra = 0
                    npar = 0
                    flag = False
                if match:
                    if match.lastgroup == "leftbracket":
                        nbra += 1
                    if match.lastgroup == "leftparenthesis":
                        npar += 1
                    if match.lastgroup == "rightbracket":
                        nbra -= 1
                    if match.lastgroup == "rightparenthesis":
                        npar -= 1

                    self._buffer = self._buffer[match.end():]
                    match = comment.search(self._buffer)
                else:
                    self._buffer = ""
                    if self._readLine():
                        match = comment.search(self._buffer)
                        if match:
                            pass #print match.lastgroup (que habia aqui Lio? creo recordar que este if no estaba simplemente pero no se)
                    else:
                        return False
            if len(self._buffer) == 0:
                self._readLine()
            return True
        else:
            self._buffer = ""
            self._readLine()
            return True

    def getPos(self):
        return (self._nline, self._tokstart)

    def yyLex(self):
        if self._readLine():
            match = self._regex.match(self._buffer)

            if match is None:
                self._buffer = self._buffer[1:]
                self._ncol += 1
                LexError(LexError.UNKNOWN_CHAR, self.getPos())
                return Token(WrapTk.TOKEN_ERROR)

            token = WrapTk.toToken(match.lastgroup)
            value = match.group(match.lastgroup)

            while token == WrapTk.COMMENT:
                if self._ignComment():
                    # Varios comentarios bien hechos separados por espacios
                    self._readLine()
                    match = self._regex.match(self._buffer)
                    if match is None:
                        return Token(WrapTk.ENDTEXT)
                    token = WrapTk.toToken(match.lastgroup)
                    value = match.group(match.lastgroup)
                else:
                    LexError(LexError.UNCLOSED_COM, self.getPos())
                    return Token(WrapTk.TOKEN_ERROR)

            self._ncol += match.end()
            self._buffer = self._buffer[match.end():]

            if token == WrapTk.ID:
                if value.lower() in self._reserved:
                    return Token(self._reserved[value.lower()])
                #if not st.isIn(value.lower()):
                #    st.insert(value.lower())
                else:
                    return Token(WrapTk.ID, value.lower())
            elif token == WrapTk.NUMERAL:
                if int(value) > 32767:
                    LexError(LexError.INT_OVERFLOW, self.getPos())
                    return Token(WrapTk.TOKEN_ERROR)
                else:
                    return Token(WrapTk.NUMERAL, int(value))
            else:   # Reconocido token valido
                return Token(token)
        else:   # Se ha llegado a fin del fichero
            return Token(WrapTk.ENDTEXT)
