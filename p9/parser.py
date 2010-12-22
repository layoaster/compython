#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Sintáctico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""
from st import *
from lexan import LexAn
from token import *
from error import *
from ffsets import *
from codegen import *

class SynAn:
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """
    MAX_LABELS = 1000

    def __init__(self, verbose = False):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner   = instancia de la clase analizador lexico
            _linerror  = almacena la linea del ultimo error mostrado (para no mostrar errores en la misma linea)
            _ff        = conjuntos de First y Follow de la gramatica de Pascal-
            _st        = Tabla de Simbolos
            _stats     = Flag para imprimir las estadisticas de la Tabla de Simbolos
        """
        # Tools
        self._scanner = None
        self._st = SymbolTable(verbose)
        self._tokenstack = Stack()
        self._exptypes = Stack()
        self._opcodestack = Stack()
        # Data
        self._ff = FFSets()
        # Variables
        self._lookahead = None
        self._labelcount = 0
        self._linerror = 0
        self._labels = -1

    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico, ordenarle abrir el
            fichero y recoger el primer token de entrada para comenzar el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
        except IOError:
            raise
        self._code = CodeGenerator(fin)
        self._lookahead = self._scanner.yyLex()
        self._program(frozenset([WrapTk.ENDTEXT]))

    def _newLabel(self):
        if self._labels > self.MAX_LABELS:
            print "FATAL ERROR: Program too large"
            exit(1)
        else:
            self._labels += 1
            return self._labels

    def _checkTypes(self, datatype, *idents):
        """ Comprueba que los identificadores tengan todos del mismo tipo (atributo datatype)
            Parametros:
                idents: identificadores a comprobar
        """
        if datatype:
            for i in idents:
                if self._st.getAttr(i.getValue(), "datatype") != datatype:
                    return False
            return True
        else:
            idtype = self._st.getAttr(idents[0].getValue(), "datatype")
            for i in idents[1:]:
                if self._st.getAttr(i.getValue(), "datatype") != idtype:
                    return False
            return True

    def _typeLength(self, datatype):
        """ Devuelve un entero con la longitud del tipo del identificador pasado por parametro
        """
        if self._st.getAttr(datatype, "kind") == WrapCl.STANDARD_TYPE:
            return 1
        elif self._st.getAttr(datatype, "kind") == WrapCl.ARRAY_TYPE:
            return (self._st.getAttr(datatype, "upperbound") - self._st.getAttr(datatype, "lowerbound") + 1) * self._typeLength(self._st.getAttr(datatype, "datatype"))
        else: # Llegados a este punto solo puede ser un record
            recordlength = 0
            for i in self._st.getAttr(datatype, "fieldlist").getIdentifiers():
                recordlength = recordlength + self._typeLength(self._st.getAttr(datatype, "fieldlist").getAttr(i, "datatype"))
            return recordlength

    def _loadProcedureLabels(self):
        proclabels = []
        for i in range(0,3):
            self._labels += 1
            proclabels.append(self._labels)
        return proclabels

    def _syntaxError(self, stop, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        if self._lookahead == WrapTk.TOKEN_ERROR:
            self._linerror = self._scanner.getPos()[0]

        if self._scanner.getPos()[0] != self._linerror:
            SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), self._lookahead, expected)
            self._linerror = self._scanner.getPos()[0]
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
            tuvo exito, se lee el siguiente token.
            En caso contrario, se llama al metodo syntaxError que se encargara de la gestion del error. Ademas,
            comprueba si el analizador lexico ha obtenido algun error durante la obtencion del token y, en tal caso,
            eleva la excepcion que este ultimo genera hacia el modulo 'pmc'.
        """
        try:
            if self._lookahead == tok:
                self._lookahead = self._scanner.yyLex()
                self._syntaxCheck(stop)
            else:
                self._syntaxError(stop)
        except LexError:
            raise

    # <Program> ::= program id ; <BlockBody> .
    def _program(self, stop):
        self._st.set()
        labels = self._loadProcedureLabels()
        labels.append(3)
        self._code.emit(WrapOp.PROGRAM, labels[0], labels[1], labels[2], labels[3])
        self._match(WrapTk.PROGRAM, stop.union((WrapTk.ID, WrapTk.SEMICOLON), self._ff.first("blockBody")))
        if self._lookahead == WrapTk.ID:
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.PROGRAM_NAME, pos=self._scanner.getPos(),ref=True):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=WrapCl.VARIABLE):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union([WrapTk.SEMICOLON], self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("blockBody")))
        self._blockBody(labels, stop)
        self._match(WrapTk.PERIOD, stop)
        #self._match(WrapTk.ENDTEXT, stop)
        self._st.reset()
        self._code.emit(WrapOp.DEFARG, 0, 0)
        self._code.emit(WrapOp.DEFARG, 0, 0)
        self._code.emit(WrapOp.ENDPROG)

    # <BlockBody> ::= [<ConstantDefinitionPart>] [<TypeDefinitionPart>] [<VariableDefinitionPart>] {<ProcedureDefinition>}
    # <CompoundStatement>
    def _blockBody(self, labels, stop):
        if self._lookahead == WrapTk.CONST:
            self._constantDefinitionPart(stop.union(self._ff.first("typeDefinitionPart"), self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.TYPE:
            self._typeDefinitionPart(stop.union(self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.VAR:
            self._variableDefinitionPart(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        while self._lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        self._compoundStatement(stop, labels[2])

    # <ConstantDefinitionPart> ::= const <ConstantDefinition> {<ConstantDefinition>}
    def _constantDefinitionPart(self, stop):
        self._match(WrapTk.CONST, stop.union(self._ff.first("constantDefinition")))
        self._constantDefinition(stop.union(self._ff.first("constantDefinition")))
        while self._lookahead == WrapTk.ID:
            self._constantDefinition(stop.union(self._ff.first("constantDefinition")))

    # <ConstantDefinition> ::= id = <Constant> ;
    def _constantDefinition(self, stop):
        # Tener cuidado con las autodefiniciones (a = a;)
        if self._lookahead == WrapTk.ID:
            self._tokenstack.push(self._lookahead)
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.CONSTANT, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("constant")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("constant")))
        self._constant(stop.union([WrapTk.SEMICOLON]))
        # Comprobacion de tipos y rellenado de informacion para las constantes
        rvalue = self._tokenstack.pop()
        lvalue = self._tokenstack.pop()
        if lvalue != WrapTk.TOKEN_ERROR:
            if rvalue != WrapTk.TOKEN_ERROR:
                if rvalue == WrapTk.NUMERAL:
                    self._st.setAttr(lvalue.getLexeme(), datatype="integer", value=rvalue.getValue())
                elif rvalue == WrapTk.ID:
                    #Verificamos que el identificador sea una constante
                    if self._st.getAttr(rvalue.getLexeme(), "kind") == WrapCl.CONSTANT:
                        idtype = self._st.getAttr(rvalue.getLexeme(), "datatype")
                        idvalue = self._st.getAttr(rvalue.getLexeme(), "value")
                        self._st.setAttr(lvalue.getLexeme(), datatype=idtype, value=idvalue)
                    elif self._st.getAttr(self._lookahead.getLexeme(), "kind") != WrapCl.UNDEFINED:
                        SemError(SemError.INVALID_KIND, self._scanner.getPos(), rvalue)
                        self._st.setAttr(lvalue.getLexeme(), datatype="NoName")
        self._match(WrapTk.SEMICOLON, stop)

    # <TypeDefinitionPart> ::= type <TypeDefinition> {<TypeDefinition>}
    def _typeDefinitionPart(self, stop):
        self._match(WrapTk.TYPE, stop.union(self._ff.first("typeDefinition")))
        self._typeDefinition(stop)
        while self._lookahead == WrapTk.ID:
            self._typeDefinition(stop)

    # <TypeDefinition> ::= id = <NewType> ;
    def _typeDefinition(self, stop):
        if self._lookahead == WrapTk.ID:
            self._tokenstack.push(self._lookahead)
            if not self._st.insert(self._tokenstack.top().getLexeme(), kind=WrapCl.UNDEFINED, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("newType")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("newType")))
        self._newType(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("typeDefinition")))
        self._tokenstack.clear()

    # <NewType> ::= <NewArrayType> | <NewRecordType>
    def _newType(self, stop):
        if self._lookahead == WrapTk.ARRAY:
            # Seteamos la clase tipo del identificador que insertamos
            self._st.setAttr(self._tokenstack.top().getLexeme(), kind=WrapCl.ARRAY_TYPE)
            self._newArrayType(stop)
        elif self._lookahead == WrapTk.RECORD:
            self._st.setAttr(self._tokenstack.top().getLexeme(), kind=WrapCl.RECORD_TYPE)
            self._newRecordType(stop)
        else:
            self._syntaxError(stop, self._ff.first("newType"))

    # <NewArrayType> ::= array [ <IndexRange> ] of id
    def _newArrayType(self, stop):
        self._match(WrapTk.ARRAY, stop.union((WrapTk.LEFTBRACKET, WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._match(WrapTk.LEFTBRACKET, stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._indexRange(stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.RIGHTBRACKET, stop.union((WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.OF, stop.union([WrapTk.ID]))
        # Tener cuidado con las autodefiniciones, Ej:
        # pepe = array [1..10] of pepe;
        arraytype = "NoName"
        if self._lookahead == WrapTk.ID:
            if self._lookahead not in self._tokenstack:
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                else:
                    arraytype = self._lookahead.getValue()
            else:
                SemError(SemError.REC_DEFINITION, self._scanner.getPos(), self._lookahead)
                arraytype = self._lookahead.getValue()
        # Insertamos los datos del array en la tabla de simbolos
        ub = self._tokenstack.pop().getValue()
        lb = self._tokenstack.pop().getValue()

        #Comprobamos que el id de tipo
        if self._st.getAttr(arraytype, "kind") in (WrapCl.ARRAY_TYPE, WrapCl.RECORD_TYPE, WrapCl.STANDARD_TYPE):
            self._st.setAttr(self._tokenstack.pop().getValue(), kind=WrapCl.ARRAY_TYPE, lowerbound=lb, upperbound=ub, datatype=arraytype)
        else:
            SemError(SemError.INVALID_KIND, self._scanner.getPos(), self._lookahead)
            self._st.setAttr(self._tokenstack.pop().getValue(), kind=WrapCl.ARRAY_TYPE, datatype="NoName", lowerbound=lb, upperbound=ub)
        self._match(WrapTk.ID, stop)

    # <IndexRange> ::= <Constant> .. <Constant>
    def _indexRange(self, stop):
        self._constant(stop.union([WrapTk.DOUBLEDOT], self._ff.first("constant")))
        self._match(WrapTk.DOUBLEDOT, stop.union(self._ff.first("constant")))
        self._constant(stop)
        # Extraemos los indices de la pila para comprobar que el rango es valido
        upperbound = self._tokenstack.pop()
        lowerbound = self._tokenstack.pop()
        # Si alguno de los indices es erroneo, se considera el rango [0..0] por defecto
        if upperbound == WrapTk.TOKEN_ERROR or lowerbound == WrapTk.TOKEN_ERROR:
            self._tokenstack.push(Token(WrapTk.NUMERAL, 0))
            self._tokenstack.push(Token(WrapTk.NUMERAL, 0))
        else:
            # Si alguno de los indices es una constante ya definida, se busca su valor
            if upperbound == WrapTk.ID and self._st.getAttr(upperbound.getValue(), "kind") == WrapCl.CONSTANT:
                upperbound = Token(WrapTk.NUMERAL, self._st.getAttr(upperbound.getValue(), "value"))
            if lowerbound == WrapTk.ID and self._st.getAttr(lowerbound.getValue(), "kind") == WrapCl.CONSTANT:
                lowerbound = Token(WrapTk.NUMERAL, self._st.getAttr(lowerbound.getValue(), "value"))
            # Comprobamos si el rango es valido. Si no, el menor toma el valor del mayor
            if upperbound.getValue() < lowerbound.getValue():
                SemError(SemError.INVALID_RANGE, self._scanner.getPos())
                upperbound.setValue(lowerbound.getValue())
            # Devolvemos los indices a la pila
            self._tokenstack.push(lowerbound)
            self._tokenstack.push(upperbound)

    # <NewRecordType> ::= record <FieldList> end
    def _newRecordType(self, stop):
        self._st.set()
        self._match(WrapTk.RECORD, stop.union([WrapTk.END], self._ff.first("fieldList")))
        self._fieldList(stop.union([WrapTk.END]))
        self._match(WrapTk.END, stop)
        #Obtenemos la TS del record para luego asignarsela como atributo
        fieldlist = self._st.top()
        self._st.reset()
        # Asignamos al recordid el atributo que contiene la lista de campos declarados (LST actual)
        self._st.setAttr(self._tokenstack.pop().getValue(), fieldlist=fieldlist)

    # <FieldList> ::= <RecordSection> {; <RecordSection>}
    def _fieldList(self, stop):
        # Almacenamos el nombre del record pasado por pila para comprobaciones
        recordid = self._tokenstack.top()
        self._recordSection(recordid, stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("recordSection")))
            self._recordSection(recordid, stop.union([WrapTk.SEMICOLON]))


    # <RecordSection> ::= id {, id} : id
    def _recordSection(self, recordid, stop):
        # Tener cuidado con las autodefiniciones, Ej:
        # paco = record
        #           campo1, campo2 : paco;
        #
        #        end;
        if self._lookahead == WrapTk.ID:
            self._tokenstack.push(self._lookahead)
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.FIELD, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
                self._tokenstack.pop()
        else:
            self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            if self._lookahead == WrapTk.ID:
                self._tokenstack.push(self._lookahead)
                if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.FIELD, pos=self._scanner.getPos()):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
                    self._tokenstack.pop()
            else:
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        idtype = "NoName"
        if self._lookahead == WrapTk.ID:
            if (self._lookahead != recordid) and (self._lookahead not in self._tokenstack):
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                elif self._st.getAttr(self._lookahead.getLexeme(), "kind") not in (WrapCl.STANDARD_TYPE, WrapCl.ARRAY_TYPE, WrapCl.RECORD_TYPE):
                    # Comprobamos que el id del tipo sea de una clase valida
                    SemError(SemError.TYPE_NOT_ALLOWED, self._scanner.getPos(), self._lookahead)
                else:
                    idtype = self._lookahead.getLexeme()
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        # Añadiendo tipos a los identificadores de campo declarados
        while len(self._tokenstack) > 1:
            if self._tokenstack.top() != WrapTk.TOKEN_ERROR:
                self._st.setAttr(self._tokenstack.pop().getLexeme(), datatype=idtype)
            else:
                self._tokenstack.pop()
        self._match(WrapTk.ID, stop)

    # <VariableDefinitionPart> ::= var <VariableDefinition> {<VariableDefinition>}
    def _variableDefinitionPart(self, stop):
        self._match(WrapTk.VAR, stop.union(self._ff.first("variableDefinition")))
        self._variableDefinition(stop.union(self._ff.first("variableDefinition")))
        while self._lookahead == WrapTk.ID:
            self._variableDefinition(stop.union(self._ff.first("variableDefinition")))

    # <VariableDefinition> ::= <VariableGroup> ;
    def _variableDefinition(self, stop):
        self._variableGroup(WrapCl.VARIABLE, stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <VariableGroup> ::= id {, id} : id
    def _variableGroup(self, kind, stop):
        if self._lookahead == WrapTk.ID:
            self._tokenstack.push(self._lookahead)
            if not self._st.insert(self._lookahead.getLexeme(), kind=kind, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))

        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            if self._lookahead == WrapTk.ID:
                self._tokenstack.push(self._lookahead)
                if not self._st.insert(self._lookahead.getLexeme(), kind=kind, pos=self._scanner.getPos()):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
                    self._tokenstack.pop()
            else:
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        idtype = "NoName"
        if (self._lookahead == WrapTk.ID):
            if self._lookahead not in self._tokenstack:
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                elif self._st.getAttr(self._lookahead.getLexeme(), "kind") not in (WrapCl.STANDARD_TYPE, WrapCl.ARRAY_TYPE, WrapCl.RECORD_TYPE):
                    # Comprobamos que el id del tipo sea de una clase valida
                    SemError(SemError.TYPE_NOT_ALLOWED, self._scanner.getPos(), self._lookahead)
                else:
                    idtype = self._lookahead.getLexeme()
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        # Añadiendo tipos a los identificadores declarados
        varlist = []
        while not self._tokenstack.isEmpty():
            if self._tokenstack.top() != WrapTk.TOKEN_ERROR:
                self._st.setAttr(self._tokenstack.top().getLexeme(), datatype=idtype)
                # Se inserta en la lista una tupla con el lexema del parametro y su tipo
                varlist.append((self._tokenstack.pop(), idtype))
            else:
                self._tokenstack.pop()
        self._match(WrapTk.ID, stop)
        if kind in (WrapCl.VAR_PARAMETER, WrapCl.VALUE_PARAMETER):
            self._tokenstack.push(varlist)

    # <ProcedureDefinition> ::= procedure id <ProcedureBlock> ;
    def _procedureDefinition(self, stop):
        self._labels += 1
        self._code.emit(WrapOp.DEFADDR, self._labels)
        self._match(WrapTk.PROCEDURE, stop.union((WrapTk.ID, WrapTk.SEMICOLON), self._ff.first("procedureBlock")))
        if self._lookahead == WrapTk.ID:
            if not self._st.insert(self._lookahead.getValue(), kind=WrapCl.PROCEDURE, pos=self._scanner.getPos(), label=self._labels):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
                procid = "NoName"
            else:
                procid = self._lookahead.getValue()
                self._st.setAttr(procid, paramlist=[])
        else:
            procid = "NoName"
        self._match(WrapTk.ID, stop.union(self._ff.first("procedureBlock"), [WrapTk.SEMICOLON]))
        self._procedureBlock(procid, stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <ProcedureBlock> ::= [( <FormalParameterList> )] ; <BlockBody>
    def _procedureBlock(self, procid, stop):
        self._st.set()
        labels = self._loadProcedureLabels()
        labels.append(self._scanner.getPos()[0])
        self._code.emit(WrapOp.PROCEDURE, labels[0], labels[1], labels[2], labels[3])
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("formalParameterList"), self._ff.first("blockBody")))
            self._formalParameterList(stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("blockBody")))
            # Esto es una lista con todos los parametros que recibe el procedimiento (puede estar vacia -> [])
            paramlist = self._tokenstack.pop()
            if procid != "NoName":
                self._st.setAttr(procid, paramlist=paramlist)
            self._match(WrapTk.RIGHTPARENTHESIS, stop.union([WrapTk.SEMICOLON], self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("blockBody")))
        self._blockBody(labels, stop)
        self._st.reset()
        self._code.emit(WrapOp.DEFARG, 0, 0)
        self._code.emit(WrapOp.DEFARG, 0, 0)
        self._code.emit(WrapOp.ENDPROC, 0)

    # <FormalParameterList> ::= <ParameterDefinition> {; <ParameterDefinition>}
    def _formalParameterList(self, stop):
        self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            previouslist = self._tokenstack.pop()
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("parameterDefinition")))
            self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))
            self._tokenstack.push(previouslist + self._tokenstack.pop())

    # <ParameterDefinition> ::= [var] <VariableGroup>
    def _parameterDefinition(self, stop):
        if self._lookahead == WrapTk.VAR:
            self._match(WrapTk.VAR, stop.union(self._ff.first("variableGroup")))
            self._variableGroup(WrapCl.VAR_PARAMETER, stop)
        else:
            self._variableGroup(WrapCl.VALUE_PARAMETER, stop)


    # <Statement> ::= id <StatementGroup> | <IfStatement> | <WhileStatement> | <CompoundStatement> | ~
    def _statement(self, stop):
        if self._lookahead == WrapTk.ID:
            if not self._st.lookup(self._lookahead.getValue()):
                SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
            elif self._st.getAttr(self._lookahead.getValue(), "kind") not in (WrapCl.CONSTANT, WrapCl.VARIABLE, WrapCl.PROCEDURE, WrapCl.STANDARD_PROC, WrapCl.VAR_PARAMETER, WrapCl.VALUE_PARAMETER):
                SemError(SemError.INVALID_KIND, self._scanner.getPos(), self._lookahead)
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
            else:
                self._tokenstack.push(self._lookahead)
            self._match(WrapTk.ID, stop.union(self._ff.first("statementGroup")))
            self._statementGroup(stop)
        elif self._lookahead == WrapTk.IF:
            self._ifStatement(stop)
        elif self._lookahead == WrapTk.WHILE:
            self._whileStatement(stop)
        elif self._lookahead == WrapTk.BEGIN:
            self._compoundStatement(stop)
        else:
            self._syntaxCheck(stop)

    # <StatementGroup> ::= {<Selector>} := <Expression> | <ProcedureStatement>
    def _statementGroup(self, stop):
        if self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES]:
            self._code.emit(WrapOp.VARIABLE, self._st.getBlockLevel(), self._st.getAttr(self._tokenstack.top().getValue(), "displ"))
            # Pasamos el tipo de id raiz a la funcion selector
            if self._tokenstack.top() != WrapTk.TOKEN_ERROR:
                #comprobamos que el id sea de la clase a la que se le pueden asignar variables
                if self._st.getAttr(self._tokenstack.top().getValue(), "kind") in (WrapCl.VARIABLE, WrapCl.VAR_PARAMETER, WrapCl.VALUE_PARAMETER):
                    self._exptypes.push(self._st.getAttr(self._tokenstack.top().getValue(), "datatype"))
                else:
                    SemError(SemError.NON_VAR_ASSIGN, self._scanner.getPos(), self._tokenstack.top())
                    self._exptypes.push("NoName")
            else:
                self._exptypes.push("NoName")
            # En caso de que no se acceda a selector ya tenemos el tipo
            ltype = self._exptypes.top()
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union([WrapTk.BECOMES], self._ff.first("selector"), self._ff.first("expression")))
                ltype = self._exptypes.top()
            #vaciamos la pila de expresiones en cualquier caso
            self._exptypes.pop()
            #vaciamos pila de tokens del ultimo selector
            self._tokenstack.pop()
            self._match(WrapTk.BECOMES, stop.union(self._ff.first("expression")))
            self._expression(stop)
            rtype = self._exptypes.pop()
            # Comprobando los tipos de una sentencia de asignacion
            if (ltype != "NoName") and (rtype != "NoName"):
                # Si los tipos son distintos damos el error
                if ltype != rtype:
                    SemError(SemError.BAD_ASSIG_TYPES, self._scanner.getPos())
                self._code.emit(WrapOp.ASSIGN, self._typeLength(rtype))
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._procedureStatement(stop)
            #print "label del procedimiento:", self._st.getAttr(self._tokenstack.top(), "label")
        # En este caso se llamo a un procedimiento sin parametros por lo que se ha de limpiar la pila para quitar el nombre de procedimiento
        else:
            self._code.emit(WrapOp.PROCCALL, 0, self._st.getAttr(self._tokenstack.top().getValue(), "label"))
            self._tokenstack.pop()
            self._syntaxCheck(stop)

    # <ProcedureStatement> ::= [( <ActualParameterList> )]
    def _procedureStatement(self, stop):
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("actualParameterList")))
            self._actualParameterList(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)

    # <ActualParameterList> ::= <Expression> {, <Expression>}
    def _actualParameterList(self, stop):
        # Nombre del procedimiento
        procid = self._tokenstack.pop().getValue()
        #Identificamos si se trata de un procedimiento definido por el usuario
        if self._st.getAttr(procid, "kind") == WrapCl.PROCEDURE:
            self._expression(stop.union([WrapTk.COMMA]))
            # Creando lista de tipos de los parametros actuales
            paramtypes = []
            if self._exptypes.top() != "NoName":
                paramtypes = [self._exptypes.pop()]
            while self._lookahead == WrapTk.COMMA:
                self._match(WrapTk.COMMA, stop.union([WrapTk.COMMA], self._ff.first("expression")))
                self._expression(stop.union([WrapTk.COMMA]))
                paramtypes.append(self._exptypes.pop())
            # Comprobamos que no sea una ID de procedimiento no declarados (TOKEN_ERROR)
            if procid != None:
                # Obtenemos lista de parametros formales
                paramlist = self._st.getAttr(procid, "paramlist")
                # Comprobamos que el numero de parametros coincida
                if len(paramlist) != len(paramtypes):
                    SemError(SemError.BAD_PARAM_NUMBER, self._scanner.getPos(), procid)
                else:
                    # Comprobamos los tipos de los parametros
                    for i in range(0, len(paramlist)):
                        formaltype = paramlist[i][1]
                        if paramtypes[i] not in ("NoName", formaltype):
                            # El parametro actual tiene un tipo distinto del parametro formal
                            SemError(SemError.BAD_PARAM_TYPE, self._scanner.getPos(), paramtypes[i], " but expected \'" + formaltype + "\' on argument no. " + str(i + 1))
                            break
        # sino se tratara de un procedimiento estandar
        elif self._st.getAttr(procid, "kind") == WrapCl.STANDARD_PROC:
            self._ioStatement(procid, stop)
        else:
            while self._lookahead != WrapTk.RIGHTPARENTHESIS:
                self._lookahead = self._scanner.yyLex()

    def _ioStatement(self, procid, stop):
        if procid == "read":
            # Verificamos que se haya puesto un ID
            if self._lookahead != WrapTk.ID:
                SemError(SemError.READ_INT_EXPCT, self._scanner.getPos())
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                self._exptypes.push("NoName")
            else:
                if self._st.lookup(self._lookahead.getValue()):
                    self._tokenstack.push(self._lookahead)
                    #Comprobamos que sea del tipo variable o constante
                    if self._st.getAttr(self._lookahead.getValue(), "kind") in (WrapCl.VARIABLE, WrapCl.CONSTANT, WrapCl.VAR_PARAMETER, WrapCl.VALUE_PARAMETER):
                        self._exptypes.push(self._st.getAttr(self._lookahead.getValue(), "datatype"))
                    else:
                        SemError(SemError.TYPE_NOT_ALLOWED, self._scanner.getPos(), self._lookahead)
                        self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                        self._exptypes.push("NoName")
                else:
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                    self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                    self._exptypes.push("NoName")
            self._match(WrapTk.ID, stop.union((WrapTk.PERIOD, WrapTk.LEFTBRACKET)))
            # En caso de que no se acceda a selector ya tenemos el tipo
            idtype = self._exptypes.top()
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union((WrapTk.BECOMES, WrapTk.END), self._ff.first("selector"), self._ff.first("expression")))
                idtype = self._exptypes.top()
            #vaciamos la pila de expresiones en cualquier caso
            self._exptypes.pop()
            #vaciamos pila de tokens del ultimo selector
            self._tokenstack.pop()
            # Comprobamos el tipo del identificador
            if idtype != "NoName":
                while self._st.getAttr(idtype, "kind") != WrapCl.STANDARD_TYPE:
                    if self._st.getAttr(idtype, "kind") != WrapCl.RECORD_TYPE:
                        idtype = self._st.getAttr(idtype, "datatype")
                    else:
                        idtype = "NoName"
                if idtype != "integer":
                    SemError(SemError.READ_INT_EXPCT, self._scanner.getPos())
        # write
        else:
            self._expression(stop.union([WrapTk.END]))
            exptype = self._exptypes.pop()
            if exptype not in ("integer", "NoName"):
                SemError(SemError.WRITE_EXPR_EXPCT, self._scanner.getPos())
            else:
                self._code.emit(WrapOp.WRITE)

    # <IfStatement> ::= if <Expression> then <Statement> [else <Statement>]
    def _ifStatement(self, stop):
        labelrealend = 0
        self._match(WrapTk.IF, stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("statement")))
        exptype = self._exptypes.pop()
        if (exptype != "boolean"):# and (exptype != "NoName"):
            SemError(SemError.BOOL_EXPR_EXPCT, self._scanner.getPos(), exptype)
        self._match(WrapTk.THEN, stop.union([WrapTk.ELSE], self._ff.first("statement")))
        labelend = self._newLabel()
        self._code.emit(WrapOp.GOFALSE, labelend)
        self._statement(stop.union([WrapTk.ELSE], self._ff.first("statement")))
        self._syntaxCheck(stop.union([WrapTk.ELSE]))
        if self._lookahead == WrapTk.ELSE:
            labelrealend = self._newLabel()
            self._code.emit(WrapOp.GOTO, labelrealend)
            self._code.emit(WrapOp.DEFADDR, labelend)
            self._match(WrapTk.ELSE, stop.union(self._ff.first("statement")))
            self._statement(stop)
        if labelrealend != 0:
            self._code.emit(WrapOp.DEFADDR, labelrealend)
        else:
            self._code.emit(WrapOp.DEFADDR, labelend)

    # <WhileStatement> ::= while <Expression> do <Statement>
    def _whileStatement(self, stop):
        labelstart = self._newLabel()
        self._code.emit(WrapOp.DEFADDR, labelstart)
        self._match(WrapTk.WHILE, stop.union([WrapTk.DO], self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union([WrapTk.DO], self._ff.first("statement")))
        exptype = self._exptypes.pop()
        if (exptype != "boolean"):# and (exptype != "NoName"):
            SemError(SemError.BOOL_EXPR_EXPCT, self._scanner.getPos(), exptype)
        self._match(WrapTk.DO, stop.union(self._ff.first("statement")))
        labelend = self._newLabel()
        self._code.emit(WrapOp.GOFALSE, labelend)
        self._statement(stop)
        self._code.emit(WrapOp.GOTO, labelstart)
        self._code.emit(WrapOp.DEFADDR, labelend)

    # <CompoundStatement> ::= begin <Statement> {; <Statement>} end
    def _compoundStatement(self, stop, begin_label=None):
        if begin_label is not None:
            self._code.emit(WrapOp.DEFADDR, begin_label)
        self._match(WrapTk.BEGIN, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
        self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
            self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        self._match(WrapTk.END, stop.union([WrapTk.PERIOD]))

    # <Expression> ::= <SimpleExpression> [<RelationalOperator> <SimpleExpression>]
    def _expression(self, stop):
        self._simpleExpression(stop.union(self._ff.first("relationalOperator")))
        #Extraemos el tipo para la expresion de la izquierda del operador
        ltype = self._exptypes.pop()
        if self._lookahead in [WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS]:
            self._relationalOperator(stop.union(self._ff.first("simpleExpression")))
            self._simpleExpression(stop)
            #Extraemos el tipo para la expresion de la derecha del operador
            rtype = self._exptypes.pop()
            if (ltype != "NoName") and (rtype != "NoName"):
                if ltype != rtype:
                    SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                    ltype = "NoName"
                # si todo va bien el tipo resultante sera un boolean
                else:
                    ltype = "boolean"
            else:
                ltype = "NoName"
        # Devolvemos el tipo resultante de las expresion completa
        self._exptypes.push(ltype)

    # <RelationalOperator> ::= < | = | > | <= | <> | >=
    def _relationalOperator(self, stop):
        if self._lookahead == WrapTk.LESS:
            self._match(WrapTk.LESS, stop)
        elif self._lookahead == WrapTk.EQUAL:
            self._match(WrapTk.EQUAL, stop)
        elif self._lookahead == WrapTk.GREATER:
            self._match(WrapTk.GREATER, stop)
        elif self._lookahead == WrapTk.NOTGREATER:
            self._match(WrapTk.NOTGREATER, stop)
        elif self._lookahead == WrapTk.NOTEQUAL:
            self._match(WrapTk.NOTEQUAL, stop)
        elif self._lookahead == WrapTk.NOTLESS:
            self._match(WrapTk.NOTLESS, stop)
        else:
            self._syntaxError(stop, self._ff.first("relationalOperator"))

    # <SimpleExpression> ::= [<SignOperator>] <Term> {<AdditiveOperator> <Term>}
    def _simpleExpression(self, stop):
        #Flag para determinar si se requerira un tipo integer al primer termino
        sign = False
        if self._lookahead in [WrapTk.PLUS, WrapTk.MINUS]:
            self._signOperator(stop.union(self._ff.first("term"), self._ff.first("additiveOperator")))
            sign = True
        self._term(stop.union(self._ff.first("additiveOperator")))
        #Extraemos el tipo para la primera expresion
        ltype = self._exptypes.pop()
        if sign:
            if (ltype != "integer") and (ltype != "NoName"):
                SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                ltype = "NoName"
        while self._lookahead in [WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR]:
            self._additiveOperator(stop.union(self._ff.first("additiveOperator"), self._ff.first("term")))
            # Obtenemos el tipo esperado segun el operador
            expectedtype = self._exptypes.pop()
            self._term(stop.union(self._ff.first("additiveOperator")))
            # Obtenemos el tipo de la expresion a la derecha del operador
            rtype = self._exptypes.pop()
            # Comprobamos que el tipo esperado no sea NoName
            if expectedtype != "NoName":
                # Comprobamos que no halla tipos erroneos
                if (ltype != "NoName") and (rtype != "NoName"):
                    #Si los 2 operandos tiene distinto tipo se produce un error
                    if ltype != rtype:
                        SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                        ltype = "NoName"
                    # Sino se comprueba que sean del tipo esperado por el operador
                    elif ltype != expectedtype:
                        SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                        ltype = "NoName"
                #Alguno de los tipos es NoName asi que seteamos el ltype para la siguiente subexpresion
                else:
                    ltype = "NoName"
            else:
                ltype = "NoName"
        # Devolvemos el tipo resultante del termino
        self._exptypes.push(ltype)

    # <SignOperator> ::= + | -
    def _signOperator(self, stop):
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
        else:
            self._syntaxError(stop, self._ff.first("signOperator"))

    # <AdditiveOperator> ::= + | - | or
    def _additiveOperator(self, stop):
        # En cada caso inserto el tipo que es esperado en la expresion que se ubica al lado izquierdo del operador
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
            self._exptypes.push("integer")
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
            self._exptypes.push("integer")
        elif self._lookahead == WrapTk.OR:
            self._match(WrapTk.OR, stop)
            self._exptypes.push("boolean")
        else:
            self._syntaxError(stop, self._ff.first("additiveOperator"))
            self._exptypes.push("NoName")

    # <Term> ::= <Factor> {<MultiplyingOperator> <Factor>}
    def _term(self, stop):
        self._factor(stop.union(self._ff.first("multiplyingOperator")))
        #Extraemos el tipo para la primera expresion
        ltype = self._exptypes.pop()
        while self._lookahead in [WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND]:
            self._multiplyingOperator(stop.union(self._ff.first("multiplyingOperator"), self._ff.first("factor")))
            # Obtenemos el tipo esperado segun el operador
            expectedtype = self._exptypes.pop()
            self._factor(stop.union(self._ff.first("multiplyingOperator")))
            # Obtenemos el tipo de la expresion a la derecha del operador
            rtype = self._exptypes.pop()
            # Comprobamos que el tipo esperado no sea NoName
            if expectedtype != "NoName":
                # Comprobamos que no halla tipos erroneos
                if (ltype != "NoName") and (rtype != "NoName"):
                    #Si los 2 operandos tiene distinto tipo se produce un error
                    if ltype != rtype:
                        SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                        ltype = "NoName"
                    # Sino se comprueba que sean del tipo esperado por el operador
                    elif ltype != expectedtype:
                        SemError(SemError.CONF_EXPR_TYPES, self._scanner.getPos())
                        ltype = "NoName"
                    # Si todo va bien, podemos emitir
                    else:
                        # Las instrucciones de DIVIDE y MODULO imprimen tambien la linea
                        if self._opcodestack.top() in (WrapOp.DIVIDE, WrapOp.MODULO):
                            self._code.emit(self._opcodestack.pop(), self._scanner.getPos()[0])
                        # Las demas (MULTIPLY y AND) no lo hacen
                        elif self._opcodestack.top() is not None:
                            self._code.emit(self._opcodestack.pop())
                        # Si se produjo un error sintactico, nos limitamos a limpiar la pila
                        else:
                            self._opcodestack.pop()
                #Alguno de los tipos es NoName asi que seteamos el ltype para la siguiente subexpresion
                else:
                    ltype = "NoName"
            else:
                ltype = "NoName"
        # Devolvemos el tipo resultante del termino
        self._exptypes.push(ltype)

    # <MultiplyingOperator> ::= * | div | mod | and
    def _multiplyingOperator(self, stop):
        # En cada caso inserto el tipo que es esperado en la expresion que se ubica al lado izquierdo del operador
        if self._lookahead == WrapTk.ASTERISK:
            self._match(WrapTk.ASTERISK, stop)
            self._exptypes.push("integer")
            self._opcodestack.push(WrapOp.MULTIPLY)
        elif self._lookahead == WrapTk.DIV:
            self._match(WrapTk.DIV, stop)
            self._exptypes.push("integer")
            self._opcodestack.push(WrapOp.DIVIDE)
        elif self._lookahead == WrapTk.MOD:
            self._match(WrapTk.MOD, stop)
            self._exptypes.push("integer")
            self._opcodestack.push(WrapOp.MODULO)
        elif self._lookahead == WrapTk.AND:
            self._match(WrapTk.AND, stop)
            self._exptypes.push("boolean")
            self._opcodestack.push(WrapOp.AND)
        else:
            self._syntaxError(stop, self._ff.first("multiplyingOperator"))
            self._exptypes.push("NoName")
            self._opcodestack.push(None)

    # <Factor> ::= numeral | id {<Selector>} | ( <Expression> ) | not <Factor>
    def _factor(self, stop):
        if self._lookahead == WrapTk.NUMERAL:
            self._exptypes.push("integer")
            self._code.emit(WrapOp.CONSTANT, self._lookahead.getValue())
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            if not self._st.lookup(self._lookahead.getLexeme()):
                SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                self._exptypes.push("NoName")
            else:
                self._tokenstack.push(self._lookahead)
                #Comprobamos que sea del tipo variable o constante
                if self._st.getAttr(self._lookahead.getValue(), "kind") in (WrapCl.VARIABLE, WrapCl.CONSTANT, WrapCl.VAR_PARAMETER, WrapCl.VALUE_PARAMETER):
                    self._exptypes.push(self._st.getAttr(self._lookahead.getValue(), "datatype"))
                    print "Emitiendo variable..."
                    self._code.emit(WrapOp.VARIABLE, self._st.getBlockLevel(), self._st.getAttr(self._tokenstack.top().getValue(), "displ"))
                else:
                    SemError(SemError.TYPE_NOT_ALLOWED, self._scanner.getPos(), self._lookahead)
                    self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                    self._exptypes.push("NoName")
            self._match(WrapTk.ID, stop.union(self._ff.first("selector")))
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union(self._ff.first("selector")))
            #vaciamos pila de tokens del ultimo selector
            print "Emitiendo value..."
            self._code.emit(WrapOp.VALUE, self._typeLength(self._exptypes.top()))
            self._tokenstack.pop()
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("expression")))
            self._expression(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)
        elif self._lookahead == WrapTk.NOT:
            self._match(WrapTk.NOT, stop.union(self._ff.first("factor")))
            self._factor(stop)
            #Comprobamos que se reciba un tipo boolean
            if self._exptypes.top() != "NoName":
                if self._exptypes.top() != "boolean":
                    SemError(SemError.TYPE_NOT_ALLOWED, self._scanner.getPos())
                    self._exptypes.pop()
                    self._exptypes.push("NoName")
        else:
            self._syntaxError(stop, self._ff.first("factor"))
            self._exptypes.push("NoName")

    # <Selector> ::= <IndexSelector> | <FieldSelector>
    def _selector(self, stop):
        if self._lookahead == WrapTk.LEFTBRACKET:
            # Si no es un array, se da un error de tipo
            if self._exptypes.top() != "NoName":
                if self._st.getAttr(self._exptypes.top(), "kind") != WrapCl.ARRAY_TYPE:
                    self._exptypes.pop()
                    self._exptypes.push("NoName")
                    SemError(SemError.NOT_ARRAY_TYPE, self._scanner.getPos(), self._tokenstack.top())
                # Si es un array, se mete en la pila su tipo
                else:
                    print "tam del array:", self._typeLength(self._exptypes.top())
                    self._exptypes.push(self._st.getAttr(self._exptypes.pop(), "datatype"))
            self._indexSelector(stop)
        elif self._lookahead == WrapTk.PERIOD:
            # Si no es un record, se da un error de tipo
            if self._exptypes.top() != "NoName":
                if self._st.getAttr(self._exptypes.top(), "kind", WrapCl.RECORD_TYPE) != WrapCl.RECORD_TYPE:
                    self._exptypes.pop()
                    self._exptypes.push("NoName")
                    SemError(SemError.NOT_RECORD_TYPE, self._scanner.getPos(), self._tokenstack.top())
                # Si es un record, se mete en la pila su tipo
                else:
                    print "tam del record:", self._typeLength(self._exptypes.top())
                    self._exptypes.push(self._st.getAttr(self._exptypes.pop(), "fieldlist", WrapCl.RECORD_TYPE))
                    self._tokenstack.pop()
            self._fieldSelector(stop)
        else:
            self._exptypes.push("NoName")
            self._syntaxError(stop, self._ff.first("selector"))

    # <IndexSelector> ::= [ <Expression> ]
    def _indexSelector(self, stop):
        self._match(WrapTk.LEFTBRACKET, stop.union([WrapTk.RIGHTBRACKET], self._ff.first("expression")))
        self._expression(stop.union([WrapTk.RIGHTBRACKET]))
        if self._st.getAttr(self._exptypes.pop(), "kind", WrapCl.STANDARD_TYPE) != WrapCl.STANDARD_TYPE:
            SemError(SemError.ILLEGAL_INDEX, self._scanner.getPos())
        self._match(WrapTk.RIGHTBRACKET, stop)

    # <FieldSelector> ::= . id
    def _fieldSelector(self, stop):
        self._match(WrapTk.PERIOD, stop.union([WrapTk.ID]))
        if self._lookahead == WrapTk.ID:
            fieldlist = self._exptypes.pop()
            if fieldlist != "NoName":
                if not fieldlist.isIn(self._lookahead.getValue()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                    self._exptypes.push("NoName")
                    self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                else:
                    self._exptypes.push(fieldlist.getAttr(self._lookahead.getValue(), "datatype"))
                    self._tokenstack.push(self._lookahead)
            else:
                self._exptypes.push("NoName")
        # En el caso que no se encuentre ningun id en el programa
        else:
            self._exptypes.push("NoName")
        self._match(WrapTk.ID, stop)

    # <Constant> ::= numeral | id
    def _constant(self, stop):
        if self._lookahead == WrapTk.NUMERAL:
            self._tokenstack.push(self._lookahead)
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            if self._lookahead not in self._tokenstack:
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
                    self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
                else:
                    self._tokenstack.push(self._lookahead)
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
                self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
            self._match(WrapTk.ID, stop)
        else:
            self._syntaxError(stop, self._ff.first("constant"))
            self._tokenstack.push(Token(WrapTk.TOKEN_ERROR))
