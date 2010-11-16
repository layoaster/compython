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
from ffsets import *
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
            _stack     = pila que almacena los atributos resultado del proceso de traduccion

        """
        self._lookahead = None
        self._scanner = None
        self._ff = FFSets()
        self._linerror = 0
        self._strTree = ""
        self._ast = AbstractSyntaxTree()
        self._stack = Stack()


    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico, ordenarle abrir el
            fichero y recoger el primer token de entrada para comenzar el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
            self._lookahead = self._scanner.yyLex()
            self._expr(frozenset([WrapTk.ENDTEXT]))
            self._ast.setRoot(self._stack.pop())
        except IOError:
            raise
        except IndexError: # Excepcion provocada al intentar hacer pop cuando la pila esta vacia
            pass
	print self._strTree

    def _syntaxError(self, stop, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        #if self._scanner.getPos()[0] != self._linerror:
        SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), self._lookahead, expected)
        #    self._linerror = self._scanner.getPos()[0]
        while self._lookahead not in stop:
            self._lookahead = self._scanner.yyLex()

    def _syntaxCheck(self, stop):
        """ Comprueba que el token siguiente este dentro de lo que puede esperarse a continuacion (el token
            pertenezca al conjunto de parada)
        """
        if self._lookahead not in stop:
            self._syntaxError(stop)

    def getDPT(self):
	""" Retorna la cadena de descripcion del arbol de analisis sintactico con adornos.
            (DPT - Decorated Parse Tree)
	"""
	return self._str

    def getAST(self):
        """ Retorna la cadena de descripcion del arbol sintactico abstracto para su representacion web
	    (AST - Abstract Syntax Tree)
        """
        return self._ast.getAST()

    def printAST(self):
        self._ast.printSequences()

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

    # <Expr> ::= <Term> {Expr2.h := Term.ptr} <Expr2> {Expr.ptr := Expr2.s}
    def _expr(self, stop):
	self._strTree += "[<Expr>_Expr.ptr:=Expr2.s"
        self._term(stop.union(self._ff.first("expr2")))
        #self._stack.push(self._ast.pop())
        self._expr2(stop)
        #self._stack.push(self._ast.pop())
	self._strTree += "]"

    # <Expr2> ::= + <Term> {Expr2.h := mknode('+', Expr2.h, Term.ptr)} <Expr2> {Expr2.s := Expr2.s}
    #           | - <Term> {Expr2.h := mknode('-', Expr2.h, Term.ptr)} <Expr2> {Expr2.s := Expr2.s}
    #           | ~ {Expr2.s := Expr2.h}
    def _expr2(self, stop):
	self._strTree += "[<Expr2>_Expr2.s:=Expr2.s"
        if self._lookahead == WrapTk.PLUS:
	    self._strTree += "^Expr2.h:=mknode('+',Expr2.h,Term.ptr)"
            self._match(WrapTk.PLUS, stop.union(self._ff.first("term"), self._ff.first("expr2")))
            self._term(stop.union(self._ff.first("expr2")))
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("+", self._stack.pop(), temp))
            self._expr2(stop)
            #self._stack.push(self._ast.pop())
        elif self._lookahead == WrapTk.MINUS:
	    self._strTree += "^Expr2.h:=mknode('-',Expr2.h,Term.ptr)"
            self._match(WrapTk.MINUS, stop.union(self._ff.first("term"), self._ff.first("expr2")))
            self._term(stop.union(self._ff.first("expr2")))
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("-", self._stack.pop(), temp))
            self._expr2(stop)
            #self._stack.push(self._ast.pop())
        else:
            self._strTree += "\bh^Expr2.h:=Term.ptr[&#248;]"
            self._syntaxCheck(stop)
            #self._stack.push(self._ast.pop())
	self._strTree += "]"

    # <Term> ::= <Factor> {Term2.h := Factor.ptr} <Term2> {Term.ptr := Term2.s}
    def _term(self, stop):
	self._strTree += "[<Term>_Term.ptr:=Term2.s"
        self._factor(stop.union(self._ff.first("term2")))
        #self._stack.push(self._ast.pop())
        self._term2(stop)
        #self._stack.push(self._ast.pop())
        self._strTree += "]"

    # <Term2> ::= * <Factor> {Term2.h := mknode('*', Term2.h, Factor.ptr)} <Term2> {Term2.s := Term2.s}
    #           | / <Factor> {Term2.h := mknode('/', Term2.h, Factor,ptr)} <Term2> {Term2.s := Term2.s}
    #           | ~ {Term2.s := Term2.h}
    def _term2(self, stop):
	self._strTree += "[<Term2>_Term2.s:=Term2.s"
        if self._lookahead == WrapTk.ASTERISK:
	    self._strTree += "^Term2.h:=mknode('*',Term2.h,Factor.ptr)"
            self._match(WrapTk.ASTERISK, stop.union(self._ff.first("factor"), self._ff.first("term2")))
            self._factor(stop.union(self._ff.first("term2")))
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("*", self._stack.pop(), temp))
            self._term2(stop)
            #self._stack.push(self._ast.pop())
        elif self._lookahead == WrapTk.SLASH:
            self._strTree += "^Term2.h:=mknode('/',Term2.h,Factor.ptr)"
            self._match(WrapTk.SLASH, stop.union(self._ff.first("factor"), self._ff.first("term2")))
            self._factor(stop.union(self._ff.first("term2")))
            temp = self._stack.pop()
            self._stack.push(self._ast.mkNode("/", self._stack.pop(), temp))
            self._term2(stop)
            #self._stack.push(self._ast.pop())
        else:
            self._strTree += "\bh^Term2.h:=Factor.ptr[&#248;]"
            self._syntaxCheck(stop)
            #self._stack.push(self._ast.pop())
	self._strTree += "]"

    # <Factor> ::= ( <Expr> ) {Factor.ptr := Expr.ptr}
    #            | - <Factor> {Factor.ptr := mkunode('-', Factor.ptr)}
    #            | id {Factor.ptr := mkleaf(id, id.ptr)}
    #            | numeral {Factor.ptr := mkleaf(num, num.ptr)}
    def _factor(self, stop):
	self._strTree += "[<Factor>"
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._strTree += "_Factor.ptr:=Expr.ptr"
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("expr")))
            self._expr(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)
            #self._stack.push(self._ast.pop())
        elif self._lookahead == WrapTk.MINUS:
	    self._strTree += "_Factor.ptr:=mkunode('-',Factor.ptr)"
            self._match(WrapTk.MINUS, stop.union(self._ff.first("factor")))
            self._factor(stop)
            self._stack.push(self._ast.mkNode("-", self._stack.pop()))
        elif self._lookahead == WrapTk.ID:
	    self._strTree += "_Factor.ptr:=mkleaf(" + self._lookahead.getLexeme() + ")"
            self._stack.push(self._ast.mkLeaf(self._lookahead.getValue()))
            self._match(WrapTk.ID, stop)
        elif self._lookahead == WrapTk.NUMERAL:
	    self._strTree += "_Factor.ptr:=mkleaf(" + self._lookahead.getLexeme() + ")"
            self._stack.push(self._ast.mkLeaf(self._lookahead.getValue()))
            self._match(WrapTk.NUMERAL, stop)
        else:
            self._syntaxError(stop)
	self._strTree += "]"
