{ Sergio Delgado Quintero
	Curso 2000-2001
	Introduccion a los Compiladores I
	Practica 1: Introduccion al Lenguaje Pascal-
	12 de Octubre de 2000
	NOTA: Perdon por el tema de las tildes (debido a lo de UNIX) }

{ Implementacion de la Convolucion Circular de 2 senales discretas.
  Dada una funcion h denominada respuesta al impulso en un sistema,
  nosotros podemos conocer la salida de cualquier entrada a ese
  sistema mediante la convolucion de la senal de entrada, en este caso
  x, con la funcion h respuesta al impulso, obteniendo una salida y.
  
  Cuando se ejecuta el programa aparece un primer "prompt" a partir
  del que empezaremos a insertar los valores enteros de la senal x,
  al realizar N inserciones, aparece un segundo "prompt" donde tendremos
  que insertar los valores de la senal h, y una vez acabado saldrá por
  pantalla el resultado, que es la convolucion -> y. 
	Cuando el programa se ejecuta en UNIX, hay problemas en cuanto a la
	visualizacion de los vectores, porque no coje el salto de carro y
	aparece una ristra de numeros que no se sabe bien que es.
	Por el contrario, si aparece bien en MS-DOS, o sea que como prefiera. } 

program Prac01;

const N = 8; { Numero de elementos de las senales }
type Senal = array[1..N] of integer; { Tipo Senal Discreta }

var
	{ x es la senal de entrada, h es la respuesta al impulso, y es la salida }
	x, h, y: Senal;

{ Procedimiento para leer una senal por teclado 
  PARAMETROS:
	u: senal en la que voy a insertar los elementos leidos.
	sep: separador para cada senal (debido a que no existen char). }
procedure LeerSenal (var u: Senal; sep: integer);
var
	i: integer;
begin
	i := 1;
  write (sep);  { Lo uso como separador }
	while (i <= N) do
		begin
			read(u[i]);
			i := i + 1;
		end;
end;

{ Procedimiento para escribir una senal por teclado 
  PARAMETROS:
	u: senal a escribir por pantalla. 
	sep: separador para cada senal (debido a que no existen char). }
procedure EscribirSenal (u: Senal; sep: integer);
var
	i: integer;
begin
	i := 1;
  write (sep); { Lo uso como separador }
	while (i <= N) do
		begin
			write(u[i]);
			i := i + 1;
		end;
end;

{ Procedimiento que coloca el vector h en su posicion inicial,
	realizando una rotacion circular y aplicando una ventana.
	PARAMETROS:
	u: senal a la que le voy a aplicar este proceso.
	Ej.
	a: [1 4 5 3]           [1 4 5 3]           [1 4 5 3]     | 1 4 5 3 | 
	b: [7 3 9 6] --> [6 9 3 7]       --> [6 9 3 7 6 9 3] --> | 7 6 9 3 | }
procedure RotyVent (var u: Senal);
var
	i: integer;
begin
  u[1] := h[1]; { el primer elemento queda igual }
	i := 2;
	while (i <= N) do
		begin
	  u[i] := h[(N - i) + 2];
			i := i + 1;
		end;
end;

{ Procedimiento que realiza una rotacion circular del vector u 
	PARAMETROS:
	u: senal a la que le voy a aplicar este proceso. }
procedure Rotar (var u: Senal);
var
	aux: Senal; { Necesito un vector auxiliar para no machacar el otro }
	i: integer;
begin
  i := 1;
	while (i <= N) do
		begin
	  aux[(i mod N) + 1] := u[i];
			i := i + 1;
		end;
	u := aux;
end;

{ Procedimiento encargado de llevar a cabo la convolucion.
  En cada iteracion se multiplica cada componente del vector de
	entrada con la funcion respuesta al impulso (debidamente colocada
	despues de la rotacion y la ventana), y la suma de todas ellas
	es la que da cada componente de la se±al de salida. } 

procedure Convolucion;
var
	h2: Senal;  { Uso una copia de h para no modificar el original }
	i, j, sum: integer;
begin
  { Coloco 'bien' el vector de trabajo }
	RotyVent(h2);
  i := 1;
	while (i <= N) do
		begin
			sum := 0;
			j := 1;
			while (j <= N) do
				begin
		  { Multiplico cada vector }
					sum := sum + (x[j] * h2[j]);
					j := j + 1;
				end;
			y[i] := sum;
	  { Despu‰s de los productos hay que rotar el vector }
			Rotar(h2);
			i := i + 1;
	end;
end;

{ Cuerpo del programa principal }
begin
	LeerSenal(x, 1111);
	LeerSenal(h, 2222);
  Convolucion;
	EscribirSenal(y, 3333);
end.
