#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Sintáctico para expresiones aritmeticas (+, -, *, /, - (unario)) parentizadas con recuperacion de errores y con Traduccion Dirigida por la Sintaxis.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""
from lexan import LexAn
from token import *
from error import *
from stack import *
from ast import *

class SynAn:
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """
    def __init__(self):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner   = instancia de la clase analizador lexico
            _strTree   = cadena que describe el arbol de analisis sintactico obtenido en notacion phpSyntaxTree
            _linerror  = almacena la linea del ultimo error mostrado (para no mostrar errores en la misma linea)
            _ast       = Arbol Sintactico resultado de la traduccion
            _stack     = pila que almacena los atributos resultado del proceso de traduccion para la construccion del AST
            _eval      = pila que almacena los atributos resultado del proceso de traduccion para dar el resultado de la expresion
            _result    = resultado de la evaluar la expresion analizada sintacticamente
        """
        self._lookahead = None
        self._scanner = None
        self._lastError = None
        self._strTree = ""
        self._stack = Stack()
        self._eval = Stack()
        self._result = 0

    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico, ordenarle abrir el
            fichero y recoger el primer token de entrada para comenzar el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
            self._lookahead = self._scanner.yyLex()
            while self._lookahead.getToken() != WrapTk.ENDTEXT:
		print self._lookahead.getLexeme(), self._lookahead.getToken(), WrapTk.TokStrings[self._lookahead.getToken()-1]
		self._lookahead = self._scanner.yyLex()
            #self._expr(frozenset([WrapTk.ENDTEXT]))
            #self._ast.setRoot(self._stack.pop())
            self._result = self._eval.pop()
        except IOError:
            raise
        except IndexError: # Excepcion provocada al intentar hacer pop cuando la pila esta vacia
            pass
        return self._lastError

    def getDPT(self):
        """ Retorna la cadena de descripcion del arbol de analisis sintactico con adornos.
            (DPT - Decorated Parse Tree)
        """
        return self._strTree

    def getAST(self):
        """ Retorna la cadena de descripcion del arbol sintactico abstracto para su representacion web
            (AST - Abstract Syntax Tree)
        """
        return self._ast.getAST()

    def printAST(self):
        """ Imprime por pantalla los tres recorridos del arbol sintactico generado, a saber: pre-orden,
            in-orden y post-orden
        """
        self._ast.printSequences()

    def getResult(self):
        """ Getter del atributo result, que almacena el resultado de evaluar la expresion
        """
        return self._result


    def _syntaxError(self, stop, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        #if self._scanner.getPos()[0] != self._linerror:
        self._lastError = SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), self._lookahead, expected)
        #    self._linerror = self._scanner.getPos()[0]
        while self._lookahead not in stop:
            self._lookahead = self._scanner.yyLex()

    def _syntaxCheck(self, stop):
        """ Comprueba que el token siguiente este dentro de lo que puede esperarse a continuacion (el token
            pertenezca al conjunto de parada)
        """
        if self._lookahead not in stop:
            self._syntaxError(stop)

    def _match(self, tok, stop):
        """ Trata de emparejar el token leido con el token que espera encontrar en cada momento. Si el matching
            tuvo exito, se lee el siguiente token (a la vez que se adjunta la descripcion del terminal en strTree).
            En caso contrario, se llama al metodo syntaxError que se encargara de la gestion del error. Ademas,
            comprueba si el analizador lexico ha obtenido algun error durante la obtencion del token y, en tal caso,
            eleva la excepcion que este ultimo genera hacia el modulo 'pmc'.
        """
        try:
            if self._lookahead == tok:
                self._strTree += "[" + self._lookahead.getLexeme() + "]"
                self._lookahead = self._scanner.yyLex()
                self._syntaxCheck(stop)
            else:
                self._syntaxError(stop)
        except LexError:
            raise
