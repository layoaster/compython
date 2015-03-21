A continuación se listan los cambios que hubo que realizar en la susodicha gramática para dejarla LL(1) (En negrita los simbolos terminales):

## Grammar ##

# _(Regla 20)_ `<Statement> ::= `**ID** `<StatementGroup> | <If_statement> | <While_statement> | <Compound_statement | ε`
> `<StatementGroup> ::= <Procedure_statement> | {<Selector>} := <Expression>`

# _(Regla 21)_ **Se elimina**

# _(Regla 22)_ `<Procedure_statement> ::= [(<Actual_parameter_list>)]`

# _(Regla 23)_ `<Actual_parameter_list> ::= <Expression> {`**,** `<Expression>} `

# _(Regla 24)_ **Se elimina**

# _(Regla 35)_ `<Factor> ::= `**NUMERAL** | **ID** `{<Selector>} | `**(** `<Expression>` **)** | **not** `<Factor>`

# _(Regla 36)_ **Se elimina**