{ **************************************************
ASIGNATURA: Compiladores I
PRACTICA 1: Introduccion al lenguaje Pascal-
OBJETIVO: Familiarizarse con la sintaxis del lenguaje Pascal-.
DESCRIPCION: Se realizara una variante del juego del "Master Mind", que consiste
en adivinar una combinacion de digitos. Para ello se introducira una clave y otro
jugador intentara adivinar la clave introducida. Se implementara un procedimiento
que reciba como argumentos la clave y la jugada, y devuelva los aciertos exactos
(digito igual y en la misma posicion) o aproximados (digito igual pero en distinta
posicion).
Como pascal- no dispone de la funcion random, la clave se definira como una constante
en el programa. Estara formada por tres digitos, cada uno de los cuales estara com-
prendido entre [2, 7]. 
 > Entrada al programa: Numeros enteros de 3 digitos.
 > Salida: Por cada acierto exacto un 1 y por cada acierto aproximado un 0. Si no se
 visualiza nada por pantalla, indica que no se han producido aciertos exactos ni
 aproximados.

Autor: Alu1743
Fecha: 6 - 10 - 2000
Bibliografia: "Problemas de programacion", Ed. Paraninfo, pag.137

Comentarios: Algunas diferencia entre el pascal- y pascal.

 > No admite numeros negativos
 > write y read no admiten un numero indefinido de parametros, solo uno.
 > La declaracion de matrices es diferente.
 > No admite sentecia vacia
 > No admite definicion de subrangos

*************************************************** }

program mmind;

const 
    
	KEY = 475;
   LENGTH = 3;		{longitud de la clave}
	ROWKEY = 1;		{fila que ocupa la clave dentro de la matriz}			
	ROWMOVE = 2;  	{fila que ocupa la jugada dentro de la matriz}
	MAXROW = 2;
   SELECT = 0;
	MAXMOVE = 5;	{numero maximo de jugadas que se permiten}

type
    
	vector = array[1..LENGTH] of integer;
   matriz = array[1..MAXROW] of vector;         

   {en la primera fila de la matriz se almacenaran los digitos }
   {de la constante KEY, y en la segunda fila los digitos de la}
   {jugada realizada.}

{ ***********************************************
digitexact: Dada la clave y la jugada se comprueba el numero de aciertos
exactos (digito igual y en la misma posicion). Se tachan aquellos digitos
que intervengan en la solucion . Para ello se utiliza la constante SELECT, 
cada vez que un digito de la jugada es escogido como digito exacto o 
aproximado, este digito se pone a cero para no volver a considerarlo en 
analizis posteriores.
************************************************* }
procedure digits_exact(var keymove: matriz; var exact: integer);
var
	i: integer;
begin
	i := 1;
	while i <= LENGTH do
	begin
   	if keymove[ROWKEY][i] = keymove[ROWMOVE][i] then
		begin
			exact := exact + 1;
         keymove[ROWKEY][i] := SELECT;
         keymove[ROWMOVE][i] := SELECT;
		end;
		i := i + 1;
	end;
end;

{ ************************************************
digitnear: Dada la clave y la jugada se determina el numero de aciertos
aproximados. Se examinaran todos los digitos de la jugada (move) que no
fueron conciderados en los aciertos aproximados.
************************************************** }
procedure digits_near(var keymove: matriz; var near: integer);
var
	i, j: integer;
begin
	i := 1;
	while i <= LENGTH do
	begin
   	if keymove[ROWMOVE][i] <> SELECT then    { si el digito no ha sido examinado }
		begin                                           
			j := 1;
         while j <= LENGTH do
			begin
        		 if keymove[ROWKEY][j] = keymove[ROWMOVE][i] then  
             begin
				 	near := near + 1;
               keymove[ROWKEY][j] := SELECT;
             end;
             j := j + 1;
			end;
		end;
		i := i + 1;
	end;
end;

{ **************************************************
init_keymove: Se almacena en un vector un entero, cada elemento del vector
se corresponde con un digito del entero.
*************************************************** }
procedure init_keymove(var keymove: matriz; number: integer; index: integer);
var
	digito,
	cociente,
	i: integer;
begin
	i := LENGTH;
	cociente := number;
	while i >= 1 do
	begin
		digito := cociente mod 10;   {ultimo digito del numero}
   	cociente := cociente div 10; {nuevo numero}
   	keymove[index][i] := digito;
   	i := i - 1;
	end;
end;

{ *****************************************************
print_ex_ne: Se visualiza por pantalla un uno por cada acierto exacto (digito
igual y en la misma posicion) y un cero por cada acierto aproximado (digito
igual pero en distinta posicion).
****************************************************** }
procedure print_ex_ne(exact, near: integer);
var 
	i: integer;

begin
    i := 1;
    while i <= near do
    begin
       write(0);
       i := i + 1;
    end;
	
    i := 1;
    while i <= exact do
    begin
       write(1);
       i := i + 1;
	end;
end;

{ ******************************************************
move_check: Se calcula el numero de aciertos exactos y aproximados de la
jugada que se le pasa al procedimiento como parametro. Antes de este calculo
se almacena la clave y la jugada en una matriz, la primera fila corresponde
a la clave y la segunda a la jugada.
******************************************************* }
procedure move_check(move: integer; var exact, near: integer);
var
    keymove: matriz;
begin
	exact := 0;
	near := 0;
	Init_keymove(keymove, KEY, ROWKEY);
   init_keymove(keymove, move, ROWMOVE);
   digits_exact(keymove, exact);       {aciertos exactos}
   digits_near(keymove, near);         {aciertos aproximados}
	print_ex_ne(exact, near);				{mostramos aciertos exactos y aproximados}
end;

{ *************************************************
Principal: Programa principal. Se saldra de la ejecucion del programa cuando
se introduzca un cero.
************************************************** }
procedure init;
var
   move,
	exact,
	near,
	j: integer;
	exit: boolean;		
begin
	exit := false;
   while (j <= MAXMOVE) and (not exit) do
   begin
  		read(move);
		if move <> 0 then		
		begin		
      	move_check(move, exact, near);
			exit := (exact = 3);			{Se adivina la clave}
       	j := j + 1;
		end
		else
			exit := true;
	end;
end;

begin
    init
end.
