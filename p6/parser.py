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
        """
        self._lookahead = None
        self._scanner = None
        self._lastError = None
        self._strTree = ""
        self._ast = AbstractSyntaxTree()
        self._stack = Stack()

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

    def getASTSequence(self):
        """ Retorna ...
        """
        return self._ast.getSequence()

    def getResult(self):
        """ Getter del atributo result, que almacena el resultado de evaluar la expresion
        """
        return self._result

    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico, ordenarle abrir el
            fichero y recoger el primer token de entrada para comenzar el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
            self._lookahead = self._scanner.yyLex()
            self._rexp1()
            self._ast.setRoot(self._stack.pop())
        except IOError:
            raise
        return self._lastError

    def _syntaxError(self, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        #self._strTree += "[TOKEN-ERROR]"
        # Si el error vino desde 'match', podemos saber que token esperariamos encontrar
        raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), self._lookahead, expected)

    def _match(self, tok):
        """ Trata de emparejar el token leido con el token que espera encontrar en cada momento. Si el matching
            tuvo exito, se lee el siguiente token (a la vez que se adjunta la descripcion del terminal en strTree).
            En caso contrario, se llama al metodo syntaxError que se encargara de la gestion del error. Ademas,
            comprueba si el analizador lexico ha obtenido algun error durante la obtencion del token y, en tal caso,
            eleva la excepcion que este ultimo genera hacia el modulo 'pmc'.
        """
        try:
            if self._lookahead == tok:
                self._lookahead = self._scanner.yyLex()
            else:
                self._syntaxError()
        except LexError:
            raise

    # <Rexp1> ::= <Rexp2> <Disjunct>
    def _rexp1(self):
        self._rexp2()
        #self._stack.push(self._stack.pop())
        self._disjunct()
        #self._stack.push(self._stack.pop())

    # <Disjunct> ::= | <Rexp2> <Disjunct>
    # <Disjunct> ::= ~
    def _disjunct(self):
        if self._lookahead == WrapTk.VERTICALBAR:
            self._match(WrapTk.VERTICALBAR)
            self._rexp2()
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("|", self._stack.pop(), temp))
            self._disjunct()
            #self._stack.push(self._stack.pop())
        else:
            pass
            #self._stack.push(self._stack.pop())

    # <Rexp2> ::= <Rexp3> <Concat>
    def _rexp2(self):
        self._rexp3()
        #self._stack.push(self._stack.pop())
        self._concat()
        #self._stack.push(self._stack.pop())

    # <Concat> ::= <Rexp3> <Concat>
    # <Concat> ::= ~
    def _concat(self):
        if self._lookahead in (WrapTk.LEFTPARENTHESIS, WrapTk.LETTER):
            self._rexp3()
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("·", self._stack.pop(), temp))
            self._concat()
            #self._stack.push(self._stack.pop())
        else:
            pass
            #self._stack.push(self._stack.pop())

    # <Rexp3> ::= ( <Rexp1> ) <KClosure>
    # <Rexp3> ::= letter <KClosure>
    def _rexp3(self):
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._rexp1()
            self._match(WrapTk.RIGHTPARENTHESIS)
            #self._stack.push(self._stack.pop())
            self._kClosure()
            #self._stack.push(self._stack.pop())
        elif self._lookahead == WrapTk.LETTER:
            self._stack.push(self._ast.mkLeaf(self._lookahead.getValue()))
            self._match(WrapTk.LETTER)
            self._kClosure()
            #self._stack.push(self._stack.pop())
        else:
            self._syntaxError()

    # <KClosure> ::= * <KClosure>
    # <KClosure> ::= ~
    def _kClosure(self):
        if self._lookahead == WrapTk.ASTERISK:
            self._match(WrapTk.ASTERISK)
            self._kClosure()
            self._stack.push(self._ast.mkNode("*", self._stack.pop()))
        elif self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS)
            self._kClosure()
            self._stack.push(self._ast.mkNode("+", self._stack.pop()))
        elif self._lookahead == WrapTk.QUESTION:
            self._match(WrapTk.QUESTION)
            self._kClosure()
            self._stack.push(self._ast.mkNode("?", self._stack.pop()))
