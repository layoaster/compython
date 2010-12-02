program Shell;
{------------------------------------------------------------------------------
 Programa Shell implementado en Pascal-
  Autor: Jaime Ventor Hernandez Gonzalez (alu1893)
  Objetivo: Ordenacion de un vector por el metodo
				Shell.
  Uso:	Se han de introducir N + 1 valores enteros
			El primero, N, corresponde al numero de elementos
			enteros que desea tenga el vector para ser ordenados
			(siendo N <= 25).
			A continuacion se han de introducir los N elementos 
			enteros que se desean introducir en el vector.
-------------------------------------------------------------------------------}
const max = 25; { Numero maximo de elementos }
type T = array[1..max] of integer;
var
  vector: T;
  k, items : integer;

{-----------------------------------------------------------------------------
Procedimiento : Shell
Entrada : A -> vector que se desea ordenar
	N -> Numero de elementos del vector
Salida : A -> Vector ordenado
Funcion : Ordena el vector A mediante el metodo Shell
Subrutinas: Cambio -> Intercambia los valores de dos posiciones que se le
		pasan por variable.
-----------------------------------------------------------------------------}
procedure Shell(var A: T; N: integer);
var
	i, j, k, Hueco: integer;

	procedure Cambio (var A,B: integer);
	var
		C: integer;
	begin
		C := A;
		A := B;
		B := C;
	end;

begin
	Hueco := N div 2;
	while Hueco > 0 do
		begin
			i := Hueco + 1;
			while i <= N do
				begin
					j := i - Hueco;
					while j > 0 do
						begin
							k := j + Hueco;
							if A[j] <= A[k] then
								j := 0
							else
								begin
									Cambio(A[j],A[k]);
									j := j - Hueco;
								end;
						end;
					i := i + 1;
				end;
			Hueco := Hueco div 2;
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
			Shell(vector, items);

{ Escritura en pantalla del vector ordenado }
			k := 1;
			while k <= items do
				begin
					write(vector[k]);
					k := k + 1
			end;
		end;
end.
