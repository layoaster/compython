{*****************************************************************************
AUTOR: Ernesto Jose Hernandez Ponz
FECHA: Jueves 19 de Octubre del 2000
TITULO: Introduccion al lenguaje Pascal-
CODIGO: Pascal-
OBJETIVO: Para familiarizarme con el lenguaje Pascal-, para el cual habre de
		  disenyar un compilador a lo largo del curso, he elaborado un
		  programa (utilizando dicho lenguaje) que distribuye las canciones de
		  un CD de musica de forma que puedan ser grabadas en una cinta de
		  duracion variable. El programa esta basado en el algoritmo Branch &
		  Bound de ramificacion y acotacion, maximizando el tiempo total de
		  grabacion y, dentro de las soluciones optimas, maximizando el tiempo
		  de grabacion de la cara A de la cinta en cuestion.
*****************************************************************************}

program comp1;

const MAXPISTAS = 20; {numero maximo de pistas que puede tener nuestro CD}

type vector = array [1..MAXPISTAS] of integer;

var
	 ta, tb, npistas: integer; {t. de las caras y num. de canciones del CD}
	 t, solucion: vector; {t. de cada cancion y la cara en que grabamos}

{*****************************************************************************
Este procedimiento esperara rercibir por teclado todos los parametros
necesarios para el correcto funcionamiento del programa, que son:
	- duracion en segundos de la cara A
	- duracion en segundos de la cara B
	 - numero de canciones de nuestro CD
	- una linea por cada cancion en la que se indicara su duracion en
segundos  
*****************************************************************************}
procedure leer_datos;
var i: integer;
begin
	 read (ta);
	 read (tb);
	 read (npistas);
	 i := 1;
	 while i <= npistas do
	 begin
		  read (t [i]);
		  i := i + 1
	 end
end;

{*****************************************************************************
Es el procedimiento fundamental del programa. En base a los datos introducidos
por el usuario inicialmente, aplicara el algoritmo de Branch & Bound para
generar un vector solucion en el que se especificara la cara en la que
deberemos grabar cada cancion para que la grabacion sea optima.
*****************************************************************************}
procedure ubicar_pistas;
var
	tmax: integer; {tiempo de grabacion de la ultima solucion encontrada}
	tmin: integer; {tiempo sobrante de la cara A en la ultima solucion}
	ubicacion: vector; {vector sobre el que se va elaborando la sol. final}

	{*************************************************************************
	Se encarga de evaluar la bondad de la solucion parcial que hemos alcanzado
	hasta la etapa actual. En este caso en concreto, la bondad sera el tiempo
	de grabacion maximo que podremos alcanzar en base a las desiciones que
	hemos tomado sobre las canciones de las etapas anteriores.
	*************************************************************************} 
	procedure estimar_bondad (newa, newb, pista: integer; var bondad: integer);
	 var i: integer;
	 begin
		  bondad := newa + newb;
		  i := pista + 1;
		  while i <= npistas do
		  begin
			   bondad := bondad + t [i]; {cogemos todas las canciones post.}
			   i := i + 1
		  end
	 end;

	{*************************************************************************
	Este es nuestro procedimiento recursivo de Branch & Bound. En cada 
	llamada a este procedimiento se decidira si incluimos en la grabacion la
	cancion de la etapa actual y en caso afirmativo en que cara se grabara.
		pista --> etapa (o cancion) actual
		olda --> duracion de la cara A hasta la etapa pista - 1
		oldb --> duracion de la cara B hasta la etapa pista - 1
	*************************************************************************} 
	procedure b_and_b (pista, olda, oldb: integer);
	 var 
		newa, newb: integer; {duracion de las caras A y B en la etapa actual}
		bondad: integer;
	 begin
		  ubicacion [pista] := 0; {1 - cara A, 2 - cara B, 3 - no se graba}
		  while ubicacion [pista] < 3 do
		  begin
			   ubicacion [pista] := ubicacion [pista] + 1;
			   newa := olda;
			   newb := oldb;
			   if ubicacion [pista] = 1 then
					newa := newa + t [pista];
			   if ubicacion [pista] = 2 then
					newb := newb + t [pista];
			   estimar_bondad (newa, newb, pista, bondad);
			   if (newa <= ta) and (newb <= tb) and (bondad >= tmax) then
			   begin
					if pista = npistas then {si estamos en la ultima etapa}
					begin
						 if (newa + newb > tmax) or ((newa + newb = tmax) and (ta - newa < tmin)) then
						 begin
							  solucion := ubicacion;
							  tmax := newa + newb;
							  tmin := ta - newa
						 end
					end
					else
						 b_and_b (pista + 1, newa, newb)
			   end
		  end
	 end;

begin
	 tmax := -1; {de esta forma encontraremos al menos una solucion mejor}
	 tmin := ta + 1; {de esta forma encontraremos al menos alguna sol. mejor}
	 b_and_b (1, 0, 0)
end;

{*****************************************************************************
Muestra por pantalla la solucion obtenida. Concretamente mostrara (separados
por ceros) las pistas seleccionadas para la cara A, el tiempo de grabacion
para dicha cara, las pistas seleccionadas para la cara B y el tiempo de
grabacion para dicha cara.
***********************************************************************************************}
procedure mostrar_solucion;
var i, tc: integer; {tc es el tiempo de grabacion de cada cara}
begin
	 i := 1;
	tc := 0;
	 while i <= npistas do
	 begin
		  if solucion [i] = 1 then
		begin
			tc := tc + t [i];     
			write (i); {mostramos las pista de la cara A}
			write (0)
		end;
		  i := i + 1
	 end;
	write (tc); {mostramos el tiempo de grabada de la cara A}
	write (0);
	 i := 1;
	tc := 0;
	 while i <= npistas do
	 begin
		  if solucion [i] = 2 then
		begin
			tc := tc + t [i];            
			write (i); {mostramos las pistas de la cara B}
			write (0)
		end;
		  i := i + 1
	 end;
	write (tc) {mostramos el tiempo de grabacion de la cara B}
end;

begin
	 leer_datos;
	 ubicar_pistas;
	 mostrar_solucion
end.
