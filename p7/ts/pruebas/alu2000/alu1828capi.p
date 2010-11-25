{****************************************************************************
   AUTOR: Luis Manuel Bethencourt Correa.
   PRACTICA: Introducci¢n al lenguaje PASCAL-.
   DESCRIPCION: Dado un n£mero como m ximo de 10 d¡gitos introducido por
   teclado, el programa devuelve un 1 ¢ 0 seg£n el n£mero sea el mismo si se
   lee de izq. a derch. como de derch. a izq. o no.
   FUNCIONAMIENTO:
                 1.- Introducir el n£mero de d¡gitos del n£mero (n).
                 2.- Introducir los n d¡gitos del n£mero.
                 3.- Devuelve :
                           0 => El n£mero no es capicua.
                           1 => El n£mero es capicua.
   FECHA: 5-10-2000.
*****************************************************************************}
program encnum;

const MAXDIG = 60;        { D¡gito m ximo }
type	digitos = [0..9];
		vector = array[1..MAXDIG] of digitos;

var numero  : vector;     { N£mero a tratar }
    capicua : boolean;    { TRUE si el n£mero es capicua }
    ndig    : integer;    { N£mero de d¡gitos }

{----------------------------------------------------------------------------
 leernumero -- Pide los d¡gitos del n£mero por pantalla y los almacena en un
 vector.
  Par metros:
       - numero : Vector en el que se devuelve el n£mero.
       - ndig : N£mero de d¡gitos del n£mero.
-----------------------------------------------------------------------------}
procedure leernumero (var numero : vector; ndig : integer);
var i : integer;

begin
    i := 1;
    while (i <= ndig) do     { Leemos el n£mero }
     begin
         read(numero[i]);
         i := i + 1;
     end;
end;

{----------------------------------------------------------------------------
 obtenermitad -- Obtiene la mitad de un n£mero atendiendo a si es par o impar:
                         - Si par => mitad = num / 2
                         - Si impar => mitad = (num / 2) + 1
  Par metros:
       - mitad : Par metro en el que nos devuelve el valor mitad.
       - num : N£mero al que se la obtiene la mitad.
-----------------------------------------------------------------------------}
procedure obtenermitad(var mitad : integer; num : integer);
var i : integer;

begin
    mitad := num div 2;
    if ((num mod 2) <> 0) then   { Si es impar }
       mitad := mitad + 1;
end;

{----------------------------------------------------------------------------
 comprobar_numero -- Recorre el n£mero hasta la mitad comparando los pares de
                     d¡gitos (1,ndig), (2,ndig-1), (3,ndig-2),....,(i,ndig-i)
                     y si alguno no coincide el resultado ser  FALSE.
-----------------------------------------------------------------------------}
procedure comprobar_numero;
var salir : boolean;
    mitad : integer;
    i     : integer;

begin
    obtenermitad(mitad, ndig);
    salir := FALSE;
    i := 0;
    { S¢lo recorremos la mitad del vector }
    while (i < mitad) AND (NOT salir) do
     begin
         { Miramos si difiere alg£n par }
         if (numero[i + 1] <> numero[ndig - i]) then
            salir := TRUE;
         i := i + 1;
     end;
    capicua := NOT salir;
end;

{----------------------------------------------------------------------------
 Cuerpo del programa.
-----------------------------------------------------------------------------}
begin
    read(ndig);                   { Leemos el n£mero de d¡gitos }
    if (ndig <= MAXDIG) then
     begin
         leernumero(numero, ndig);
         comprobar_numero;        { Comprobamos si es capic£a }
         if (capicua) then
            write(1)
         else
            write(0); 
     end;
end.

