#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Representacion de los Simbolos No Terminales.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapNT:

    PROGRAM         = "program"
    BLOCKBODY       = "blockBody"
    CONSTDEFPART    = "constantDefinitionPart"
    CONSTDEF        = "constantDefinition"
    CONSTDEF2       = "constantDefinition2"
    TYPEDEFPART     = "typeDefinitionPart"
    TYPEDEF         = "typeDefinition"
    TYPEDEF2        = "typeDefinition2"
    NEWTYPE         = "newType"
    NEWARRAYTYPE    = "newArrayType"
    INDEXRANGE      = "indexRange"
    NEWRECTYPE      = "newRecordType"
    FIELDLIST       = "fieldList"
    FIELDLIST2      = "fieldList2"
    RECSECTION      = "recordSection"
    RECSECTION2     = "recordSection2"
    VARDEFPART      = "variableDefinitionPart"
    VARDEF          = "variableDefinition"
    VARDEF2         = "variableDefinition2"
    VARGROUP        = "variableGroup"
    VARGROUP2       = "variableGroup2"
    PROCDEF         = "procedureDefinition"
    PROCBLOCK       = "procedureBlock"
    PROCBLOCK2      = "procedureBlock2"
    FORPARAMLIST    = "formalParameterList"
    PARAMDEF        = "parameterDefinition"
    PARAMDEF2       = "parameterDefinition2"
    STATEMENT       = "statement"
    STATEGROUP      = "statementGroup"
    PROCSTATE       = "procedureStatement"
    ACTPARAMLIST    = "actualParameterList"
    EXPRESSION2     = "expression2"
    IFSTATE         = "ifStatement"
    IFSTATE2        = "ifStatement2"
    WHILESTATE      = "whileStatement"
    COMPSTATE       = "compoundStatement"
    STATEMENT2      = "statement2"
    EXPRESSION      = "expression"
    EXPRGROUP       = "expressionGroup"
    RELATOPER       = "relationalOperator"
    SIMPLEXPR       = "simpleExpression"
    SIMPLEXPRGROUP  = "simpleExpressionGroup"
    SIGN            = "sign"
    SIGNOPER        = "signOperator"
    ADDIOPER        = "additiveOperator"
    TERM            = "term"
    MULTIPLYING     = "multiplying"
    MULTIPLYOPER    = "multiplyingOperator"
    FACTOR          = "factor"
    FACTOR2         = "factor2"
    SELECTOR        = "selector"
    INDEXSELECTOR   = "indexSelector"
    FIELDSELECTOR   = "fieldSelector"
    CONSTANT        = "constant"

class NonTerm:

    def __init__(self, nt = None):
        """ Constructor de la clase
            _name = nombre del simbolo no terminal
        """
        self._name = nt


    def setName(self, nt):
        """ Setter del nombre del simbolo no terminal
        """
        self._name = nt

    def getName(self):
        """ Getter del nombre del simbolo no terminal
        """
        return self._name

    def __eq__(self, nt):
        """ Sobrecarga del operador de comparacion "igual que", para establecer las comparaciones entre objetos NoTerm
            tambien necesaria para utilizarlo como clave en los diccionarios
        """
        if self._name == nt.getName():
            return True
        else:
            return False

    def __hash__ (self):
        """ Sobrecarga de la funcion hash (identificando el objeto NoTerm de manera unica) necesaria para utilizarlo
            como clave en los diccionarios
        """
        return hash(self._name)
