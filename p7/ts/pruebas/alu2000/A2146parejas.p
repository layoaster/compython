{*****************************************************************************
	Autor: Zebenzui Perez Ramos
	Asignatura: Introduccion a los compiladores I
	Curso: 2000-2001
	Objetivo: La familiarizacion con el lenguaje Pascal-, un subconjunto de 
			Pascal, para el cual vamos a diseñar un compilador.
	Descripcion: Juego de memoria diseñado en pascal- que consiste en descubrir 
			parejas de numeros ocultas en un vector. El jugador debe introducir dos	
			numeros que se corresponden con las casillas del vector que desea
			levantar, una vez levantadas las casillas, si los numeros son iguales 
			permanecen visibles al jugador y si no se ocultan de nuevo.
	Observaciones: debido a la escases de pascal- la interaccion con el usuario
			no es lo buena que deberia ser.
******************************************************************************}

program parejas;

const
   MAXVECT = 12;   {Longitud maxima del vector}
   TR1 = 3;        {Tramo uno del vector para introducir la 1 parte del patron}
   TR2 = 6;        {Idem pero para el 2 tramo}
   TR3 = 9;        {Idem pero para el 3 tramo} 
   MAXPOS = 6;    {Numero de jugadas}

type
   t_vect = array [1..MAXVECT] of integer;

var
   vect : t_vect;
   ocult : t_vect;

{****************************************************************************
Procedimiento que inicializa el vector de casillas
****************************************************************************}
procedure ini_vect;
var
   i : integer;

begin
	i := 1;
   while (i <= MAXVECT) do
		begin
			vect[i] := 0;
			i := i + 1;
		end;
end;

{***************************************************************************
Procedimiento que distribuye las parejas de numeros en el vector siguiendo 
diversos patrones
***************************************************************************}
procedure ini_oculto;
var
   i : integer;

begin
	i := 1;
	{casillas pares del 2 al 6 con los num pares del 6 al 2}
   while (i <= TR1) do
		begin
         ocult[2 * i] := (TR1 * 2) - (2 * (i - 1));
			i := i + 1;
		end;
	{casillas pares del 8 al 12 con los num impares del 1 al 5}
   while (i <= TR2) do
		begin
         ocult[2 * i] := (i - TR1) + (i - (TR1 + 1));
			i := i + 1;
		end;
	{casillas impares del 1 al 5 con los impares del 1 al 5}
   while (i <= TR3) do
		begin
         ocult[(i - TR2) + (i - (TR2 + 1))] := (i - TR2) + (i - (TR2 + 1));
			i := i + 1;
		end;
	{casillas impares del 7 al 11 con los pares del 2 al 6}
   while (i <= MAXVECT) do
		begin
         ocult[(i - TR1) + (i - (TR3 + 1))] := (i - (TR3 - 1)) + (i - (TR3 + 1));
			i := i + 1;
		end;
   
end;

{**********************************************************************
Procedimiento que muestra el vector de casillas y las casillas que se
deben levantar.
Parametros:
	first: primera casilla del vector a levantar
	last: segunda casilla del vector a levantar
	idem: indica si los elementos son iguales
**********************************************************************}
procedure mostrar (first : integer; last : integer; idem : boolean);
var
   i : integer;

begin
	i := 1;
   while (i <= MAXVECT) do
		begin
         if (idem = false) then
            begin
            if (i = first) then
               write (ocult[i])
            else
               begin
               if (i = last) then
                  write (ocult[i])
               else
                  write (vect[i]);
               end;
            end
         else
            write (vect[i]);
			i := i + 1;
		end;
end;

{***********************************************************************
Procedimiento coordinador que se encarga de leer los num que el jugador
elija y levantar las casillas correspondientes. Ademas si el jugador
descubre una pareja, esa pareja queda visible siempre al jugador.
***********************************************************************}
procedure parejas;
var
   primero : integer;   {Primera casilla a levantar}
   segundo : integer;   {Segunda casilla a levantar}
   k : integer;         {Numeros de posibilidades del jugador}
   iguales : boolean;   {Indica si se ha descuierto una pareja}

begin
   k := 1;
   while (k < MAXPOS) do
   begin
      iguales := false;
      read (primero);
      read (segundo);
		if (primero <> segundo) then
		begin
      	if (ocult[primero] = ocult[segundo]) then
         	begin
            	vect[primero] := ocult[primero];
            	vect[segundo] := ocult[segundo];
            	iguales := true;
         	end;
      	mostrar (primero, segundo, iguales);
			write (-1);
      	mostrar (primero, segundo, true);
      	k := k + 1;
		end;
   end;
end;

begin
   ini_oculto;
   ini_vect;
	mostrar (1, 2, true);
   parejas;
end.

