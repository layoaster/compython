program burbuja;
{-----------------------------------------------------------------------------
 Programa Burbuja implementado en Pascal-
  Autor: Jaime Ventor Hernandez Gonzalez (alu1893)
  Objetivo: Ordenacion de un vector por el metodo
				de la burbuja.
  Uso:	Se han de introducir N + 1 valores enteros
			El primero, N, corresponde al numero de elementos
			enteros que desea tenga el vector para ser ordenados
			(siendo N <= max).
			A continuacion se han de introducir los N elementos 
			enteros que se desean introducir en el vector.
------------------------------------------------------------------------------}
const max = 25; { Numero maximo de elementos}
type T = array[1..max] of integer;
var
  vector: T;
  k, items : integer;
{-----------------------------------------------------------------------------
Procedimiento: Burbuja
Entrada: A -> vector que se desea ordenar
	N -> Numero de elementos del vector
Salida: A -> Vector ordenado
Funcion: Ordena el vector A mediante el metodo de la Burbuja.
Subrutinas: Cambio -> Intercambia los valores de dos posiciones que se le
		pasen por variable.
------------------------------------------------------------------------------}
procedure Burbuja(var A: T; N: integer);
var
	i, j: integer;

	procedure Cambio (var A,B: integer);
	var
		C: integer;
	begin
		C := A;
		A := B;
		B := C;
	end;

begin
	i := 2;
	while i <= N do
		begin
			j := N;
			while j > (i - 1) do
				begin
					if A[j - 1] > A[j] then
						Cambio(A[j],A[j - 1]);
					j := j - 1;
				end;
			i := i + 1;
		end;
end;

begin
{ Lectura del numero de elementos que va a tener el vector }
	read(items);
	if items <= max then { Con esto se controla que no se introduzcan
				mas elementos que la capacidad del vector }
		begin

{ Lectura de los elementos del vector }
			k := 1;
			while k <= items do
				begin
					read(vector[k]);
					k := k + 1
				end;
			Burbuja(vector, items);

{ Escritura en pantalla del vector ordenado }
			k := 1;
			while k <= items do
				begin
					write(vector[k]);
					k := k + 1
			end;
		end;
end.
