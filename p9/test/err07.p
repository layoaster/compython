program test_EBNF1;
begin
a := 1
a := 2;
a := 3
a := 4;
end.

{
FINALIDAD:
Probar el comportamiento del recuperador de errores con sentencias de la
forma:

compound_statement -> "begin" statement {";" statement } "end"
}
