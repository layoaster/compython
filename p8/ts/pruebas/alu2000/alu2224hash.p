{ Progama HASH.P creado por David Julian Carrasco Diaz como practica
en la asignatura INTRODUCCION A LOS COMPILADORES I en el curso 2000-2001.
	El consiste en la insercion en una tabla hash de una serie de valores intro-
ducidos por teclado, dando como resultado la tabla utilizada para guardar los   datos y el numero de colisiones ocurridas en cada posicion de la tabla, asi 
como el numero de colisiones totales. Si no se puede introducir un dato en su
posicion segun la funcion hash, se recorre a partir de esta posicion toda la
tabla secuencialmente y se inserta en el primer hueco encontrado.
	El programa se ha hecho en Pascal-, un lenguaje que consiste en un Pascal al
que se le han quitado diversas instrucciones, por lo que la presentacion 
durante la ejecucion es algo obtusa. Por tal motivo, se presenta a continuacion las operaciones que hay que hacer para su funcionamiento :
	1. Se ejecuta el programa a traves del programa interpre.
	2. Se introducen los numero uno a uno por teclado.
	3. Se muestra el numero de colisiones total ocurridas.
	4. Se muestran los componente de la tabla hash.
	5. Se muestran de forma ordenada las colisiones ocurridas en cada posicion de la tabla hash. 
	Despues de las operaciones 3, 4 y 5 hay que introducir un numero para que 
continue la ejecucion. Dos datos escritos seguidos se separan a traves de un -1.}

program hasing;
const
  TAMANO   = 13;		{Tamano de la tabla hash.}
  NULO	   = 99;	  {Valor con el que se simboliza un vacio en la tabla hash}
  CANTIDAD = 14;		{Numero de elementos a insertar en la tabla.}
type  vector = array [0..TAMANO] of integer;
							{Vector con el que se construye la tabla hash y la de colisiones.}
var
  num, 				{Numero insertado}
	numcolis,		{Numero de colisiones total.}
	j        		{Contador}	
					: integer;
  tabla_hash, {Tabla hash}
	tabla_colis {Tabla en la que se introducen las colisiones por posicion.}
					: vector;

{Procedimiento que calcula la posicion que debe ocupar un dato en la tabla hash}
procedure hash (num : integer; var posicion : integer); 
begin
	posicion := num mod TAMANO;	
end;

{Procedimiento que inserta, si es posible, un dato nuevo en la tabla hash.}
procedure insertar (num : integer; var tabla_hash : vector; 
									var vec_colis : vector; var num_colis : integer);
var
  i, pos_actual, posicion : integer;

begin
  posicion := 0;
  hash (num, posicion);
			{El dato se introduce en la posicion segun la funcion hash.}
  if (tabla_hash[posicion] = NULO) then
    tabla_hash[posicion] := num
  else
			{La posicion correspondiente al dato esta ocupada.}
  begin
    vec_colis[posicion] := vec_colis[posicion] + 1;
    num_colis := num_colis + 1;
    i := posicion + 1;
			{Se busca la primera posicion vacia.}
    while (tabla_hash[i] <> NULO) and (posicion <> i) do
      i := (i + 1) mod TAMANO;
				{Si la tabla no esta llena.}
    if tabla_hash[i] = NULO then
      tabla_hash[i] := num;
  end;
end;

{Procedimiento que inicializa la tabla hasing y las variables que guardan
informacion sobre las colisiones producidas.}
procedure iniciar (var num_colis : integer; var tabla_hash : vector;
                   var tabla_colis : vector);
var i : integer;

begin
  num_colis := 0;
  i := 0;
  while (i <= TAMANO) do
  begin
    tabla_hash[i] := NULO;
    tabla_colis[i] := 0;
    i := i + 1;
  end;
end;

{Procedimiento que muestra los datos por pantalla.}
procedure resultados (var num_colis : integer; var tabla_hash : vector;
                     var tabla_colis : vector);
var i : integer;	{Contador}

begin
		{Muestra el numero de colisiones}
	write (num_colis);
  read (i);
  i := 0;
		{Muestra la tabla hash.}
  while (i < TAMANO) do
  begin
		if (tabla_hash[i] <> NULO) then
		begin
    	write (tabla_hash[i]);
			write (-1);
		end
		else
		begin
			write (0);
			write (-1);
		end;
    i := i + 1;
  end;
	read (i);
		{Muestra el numero de colisiones en cada posicion}
  i := 0;
  while (i < TAMANO) do
  begin
    write (tabla_colis[i]);
		i := i + 1;
		write (-1);
  end;
	read (i);
end;

begin
  j := 1;
  iniciar (numcolis, tabla_hash, tabla_colis);
  while (j <= CANTIDAD) do
  begin
		write (j);
    read (num);
    insertar (num, tabla_hash, tabla_colis, numcolis);
    j := j + 1;
  end;
  resultados (numcolis, tabla_hash, tabla_colis);
end.



