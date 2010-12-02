{ PROGRAMA ADIVINA - Pract1 -
  Autor: Ivan Jesus Correa Negrin
  Centro Superior de Informatica
  17/10/2000
  Asignatura : Introduccion a los Compiladores I
  N de practica : 1
  Plataforma usada : UNIX. Programado en Pascal-
	Nota: Pascal- es un lenguaje subconjunto del Pascal. Posee su misma
  sintaxis, excluyendo numerosos tipos de datos (solo existen integer y
  boolean), funciones, y por supuesto, todas las units propias del Pascal;

  Funcionalidad del programa:
	Se trata de implementar un sencillo juego entre dos jugadores:
	  --> Un primer jugador A introduce un numero, cifra a cifra, de como
	  maximo 10 cifras. (Nota: cada vez que te solicite una cifra, pulsa
	  RETURN. Para dejar de introducir cifras, mete el 0. Los numeros, por
	  tanto, tendran 9 cifras diferentes - no el 0 -).
	  --> A continuacion, el jugador B introduce su numero, mediante el
	  mismo procedimiento. Con este numero, tratara de averiguar el lanzado
	  por el jugador A. (Nota: solo se dejara introducir tantas cifras como
	  m ximo haya introducido el jugador A; si quedaran cifras sin meter,
	  se truncar¡an las cifras de A, comenzando por el final).
	  --> Luego, el programa devolver tres valores, separados por un -1:
	  el primero, ser el n§ de cifras que no ha introducido A; el segundo,
	  el n§ de cifras que s¡ ha introducido A, pero no estn en su sitio, y
	  el tercero, ser el n§ de cifras introducidas por A, y bien colocadas.
	  El juego acabar, cuando el jugador B acierte del todo, o ste
	  introduzca el 0 en la primera cifra.

  Idea original: la idea original del programa era hacer lo mismo, pero
	  haciendo que el jugador A no fuera un player, sino la computadora.
	  Debido a la escasez de conocimientos necesarios y de mayor potencia
	  del lenguaje, no pudimos generar numeros aleatorios, necesarios para
	  ello.

  Nota: el programa compila en ambas plataformas: DOS y UNIX, pero en esta
  £ltima no ejecuta, o mejor dicho, lo hace mal.
}
program adivina;
const
  MAX_NUM = 10;  { Maximo tamano del vector numerico }
  LIM_INF =  0;
  LIM_SUP =  9;
type
	{ Vector donde guardaremos un entero cifra a cifra }
	t_adivinanza = array [1..MAX_NUM] of integer;
	t_numeros    = record
	   n_pedidos  : t_adivinanza;
	   n_adivinar : t_adivinanza;
	   longitud   : integer
	end;  { guarda el vector con el entero a adivinar y el vector con el
			entero suministrado por el usuario }
var
	numeros : t_numeros;
	acabado : boolean;
	ok      : integer;

{ ************************************************************************* }
{ Lee el numero dado por el usuario desde teclado, guardando cifra a cifra
en un vector; se dejan de introducir cifras si superamos longitud, o si
metemos un 0 (numeros con cifras <> de 0) }
procedure leer_numero (var number : t_adivinanza; var longitud : integer);
var
   i, aux : integer;
   terminado : boolean;   { indica fin o no de entrada del numero}
begin
   i := 1;
   terminado := FALSE;

   while ((i <= MAX_NUM) and (terminado = FALSE)) do
   begin
	 aux := MAX_NUM;
	 while ((aux < LIM_INF) or (aux > LIM_SUP)) do  { leemos una sola cifra }
	   read (aux);
	 if ((aux = 0) or (i >= longitud)) then { si salimos o superamos longitud }
		 terminado := TRUE;
	 if (aux <> 0) then
	 begin
	   number[i] := aux;  { metemos cifra en vector }
	   i := i + 1;
	 end;
   end;
   longitud := i - 1;
end;
{ ********************************************************************** }
{ Llama a la rutina de leer_numero para obtener los dos que nos interesan }
procedure dar_numeros (var numeros : t_numeros);
var
  longitud : integer;
begin
  longitud := MAX_NUM;
  leer_numero (numeros.n_adivinar, longitud);
  leer_numero (numeros.n_pedidos, longitud);
  numeros.longitud := longitud;
end;
{ *********************************************************************** }
{ Compara los dos numeros guardados en el record t_numeros
  numeros-> estructura donde se guardan los numeros y su longitud
  ok     -> indica el numero de cifras acertadas y en su posicion }
procedure comp_numeros (numeros : t_numeros; var ok : integer);
type
  t_flag = array [1..MAX_NUM] of boolean;  { array de bandera }
var
  i, j, posicion,
  mal,            { guarda num de cifras mal colocadas y que no estan  }
  existe,             { guarda num de cifras que estan, pero mal colocadas }
  cifra : integer;    { es la cifra actual de que se esta revisando }
  si_existe: boolean;  { indica si la cifra esta en numero, pero no en su sitio }
  solucion : t_flag;  { indica las cifras que se ha adivinado correctamente }
  mal_col  : t_flag;  { indica cifras que estan mal colocadas en el numero }

  { Procedimiento de inicializacin de vectores de flags }
  procedure inic_flag (longitud : integer; var vec_flag : t_flag);
  var
	i : integer;
  begin
	 i := 1;
	 while (i <= longitud) do
	 begin
		vec_flag[i] := FALSE;
		i := i + 1;
	 end;
  end;

  { Procedimiento general de inicializacion de variables }
  procedure iniciar (var i, mal, ok, existe : integer; longitud : integer;
					 var solucion : t_flag);
  begin
	i      := 1;
	mal    := longitud;
	ok     := 0;
	existe := 0;
	inic_flag (longitud, solucion);
	inic_flag (longitud, mal_col);
  end;

  { Muestra la solucion final }
  procedure ver_sol (mal, ok, existe : integer);
  begin
	 write (mal);
	 write (-1);        { Escribimos separador (-1) }
	 write (existe);
	 write (-1);        { Separador (-1) }
	 write (ok);
  end;

  { Si efectivamente si_existe nos da TRUE, es que esa cifra existe, pero
  esta mal colocada }
  procedure actual_existe (si_existe : boolean; var existe, mal : integer;
						  cifra: integer; var mal_col : t_flag);
  begin
	 if (si_existe = TRUE) then
	 begin
		existe := existe + 1;
		mal    := mal - 1;    { disminuimos la cantidad de incorrectas }
		mal_col[cifra] := TRUE;
	 end;
  end;

begin
  iniciar (i, mal, ok, existe, numeros.longitud, solucion);

  {Primero, contamos solo las correctas y lo indicamos en el vector de flags }
  while (i <= numeros.longitud) do
  begin
	 if (numeros.n_adivinar[i] = numeros.n_pedidos[i]) then
	 begin
		solucion[i] := TRUE;  { marcamos el vector }
		ok := ok + 1;
		mal := mal - 1;
	 end;
	 i := i + 1;
  end;

  { Mediante un bucle while anidado, distinguimos los errores de las
  cifras mal colocadas }
  i := 1;
  while (i <= numeros.longitud) do
  begin
	j := 1;
	si_existe := FALSE;
	cifra := numeros.n_adivinar[i];
	while ((j <= numeros.longitud) and (si_existe = FALSE) and
		  (solucion[i] = FALSE)) do
	begin
	  { Recorremos el vector del jugador B e ignoramos las que ya hemos
	  declarado como correctas y las declaradas como mal colocadas}
	  if ((cifra = numeros.n_pedidos[j]) and (solucion[j] = FALSE) and
		 (mal_col[j] = FALSE)) then
			si_existe := TRUE;
	  j := j + 1;
	end;
	{ Actualizamos el numero de cifras correctas mal colocadas }
	actual_existe (si_existe, existe, mal, j - 1, mal_col);
	i := i + 1;
  end;
  ver_sol (mal, ok, existe);
end;
{ ************************************************************************** }
{ Funcion principal - MAIN - }
begin
   dar_numeros (numeros);
   ok := 0;
   acabado := FALSE;
   { acabado sera FALSE hasta que el usuario haya acertado el numero o
   introduzca un cero al teclear la primera cifra }
   while ((acabado = FALSE) and (numeros.longitud <> 0)) do
   begin
	 comp_numeros (numeros, ok);  { Comparamos numeros, y vemos lo ocurrido }
	 if (ok <> numeros.longitud) then { si no hemos acertamos de pleno }
		leer_numero (numeros.n_pedidos, numeros.longitud)
	 else
	   acabado := TRUE;
   end
end.
