#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string
import re

class LexAn:

    __fin = None
    __nline = None
    __ncol = None
    __line = None

    __id = None
    __numeral = None
    __leftcomment = None
    __rightcomment = None
    __notequal = None
    __notgreater = None
    __notless = None
    __becomes = None
    __doubledot = None
    __compare = None
    __arithmetic = None
    __parenbra = None
    __punctuation = None

    def __init__(self):
        """ Constructor de la clase
        """
        self.__nline = 1
        self.__ncol = 1
        self.__line = []
        self.__fin = False
        #Patrones para los tokens
        self.__id = re.compile('[a-zA-Z]+([0-9]|_|[a-zA-Z])*', re.U)
        self.__numeral = re.compile('\d+', re.U)

        self.__becomes = re.compile(':=', re.U)
        self.__doubledot = re.compile('\.\.', re.U)
        self.__punctuation = re.compile(',|\.|:|;', re.U)



        self.__leftcomment = re.compile("\(\*|\{", re.U)
        self.__rightcomment = re.compile('\*\)|\}', re.U)

        self.__parenbra = re.compile('\(|\)|\[|\]', re.U)
        self.__arithmetic = re.compile('\+|-|\*', re.U)

        self.__notequal = re.compile('\<\>', re.U)
        self.__notgreater = re.compile('<=', re.U)
        self.__notless = re.compile('>=', re.U)
        self.__compare = re.compile('\<|=|\>', re.U)





    def openFile(self, fin):
        error = False
        try:
            self.__fin = open(fin, "rU")
        except IOError:
            error = True
        return error


    def yyLex(self):
        if self.__fin:
            self.__line = self.__fin.readline().decode("utf-8")
            while self.__line:
                # Identificadores
                token = self.__id.match(self.__line)
                if token:
                    print token.group(0)
                    #Buscamos si es una palabra reservada
                else:
                    # Digito
                    token = self.__numeral.match(self.__line)
                    #print "CHIVATAZO"
                    if token:
                        print token.group(0)
                    else:
                        # :=
                        token = self.__becomes.match(self.__line)
                        if token:
                            print token.group(0)
                        else:
                            # ..
                            token = self.__doubledot.match(self.__line)
                            if token:
                                print token.group(0)
                            else:
                                # ,|.|;|:
                                token = self.__punctuation.match(self.__line)
                                if token:
                                    print token.group(0)
                                else:
                                    # Comentario cerrado
                                    token = self.__rightcomment.match(self.__line)
                                    if token:
                                        print token.group(0) + "TOKEN_ERROR"
                                    else:
                                        # Comentario abierto
                                        token = self.__leftcomment.match(self.__line)
                                        if token:
                                            print token.group(0)
                                        else:
                                            # Parentesis y Corchetes
                                            token = self.__parenbra.match(self.__line)
                                            if token:
                                                print token.group(0)
                                            else:
                                                # Operadores Aritmeticos
                                                token = self.__arithmetic.match(self.__line)
                                                if token:
                                                    print token.group(0)
                                                else:
                                                    # <>
                                                    token = self.__notequal.match(self.__line)
                                                    if token:
                                                        print token.group(0)
                                                    else:
                                                        # <=
                                                        token = self.__notgreater.match(self.__line)
                                                        if token:
                                                            print token.group(0)
                                                        else:
                                                            # <>
                                                            token = self.__notless.match(self.__line)
                                                            if token:
                                                                print token.group(0)
                                                            else:
                                                                # <|=|>
                                                                token = self.__compare.match(self.__line)
                                                                if token:
                                                                    print token.group(0)

                self.__line = self.__fin.readline().decode("utf-8")
                self.__nline += 1

            self.__fin.close()
        else:
            print "ERROR: no se ha abierto el fichero de codigo fuente."
            exit(-1)


# --- Programa Principal ---
if __name__ == '__main__':

    analex = LexAn()
    analex.openFile(sys.argv[1])
    analex.yyLex()

