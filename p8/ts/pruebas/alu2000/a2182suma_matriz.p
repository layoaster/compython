{ ----------------------------------------
	* Programa de prueba para Pascal-
	Fecha: 16/10/2000
	Alumno: Vargas Ruiz, Fco.
	Asignatura: Introd. a los compiladores I
	* Descripcion: Suma matrices de 2x2
	Primero se introduce el num. de filas de las matrices,
	luego el numero de columnas, y despues metemos 'filasXcolumnas'
	valores para rellenar la matriz, y esto dos veces (una vez para
	cada matriz). Los datos se van metiendo por filas. El resultado
	se muestra del mismo modo que se introdujeron los datos (por filas)
  ---------------------------------------- }
program suma;

const
	MAXX = 20;	{ num maximo de columnas de la matriz }
	MAXY = 20;	{ num maximo de filas de la matriz }
	SEPARADOR = 1;

type 
	tvector = array [1..MAXX] of integer; { definicion del tipo vector }
	tmatriz = array [1..MAXY] of tvector; { def. de matriz }

var
	matA, matB, matResult : tmatriz;
	fil, col : integer;

{ introducir los datos en la matriz desde teclado
	nota: los datos los pide por filas }
procedure intro_matriz(var matriz:tmatriz; var fil, col:integer);
var cont1, cont2:integer;
begin
	cont1:=1;
	while (cont1<=col) do
	begin
		cont2:=1;
		while (cont2<=fil) do
		begin
			read(matriz[cont2][cont1]);
			cont2 := cont2+1;
		end;
		cont1 := cont1+1;
	end;
end;

{ mostrar los elementos de la matriz en pantalla 
	nota: los datos se muestran en una sola fila y sin separacion }
procedure mostrar_matriz(matriz:tmatriz;fil,col:integer);
var cont1, cont2:integer;
begin
	cont1:=1;
	while (cont1<=col) do
	begin
		cont2:=1;
		while (cont2<=fil) do
		begin
			write(SEPARADOR*matriz[cont2][cont1]);
			cont2:=cont2+1;
		end;
		cont1:=cont1+1;
	end;
end;

{ suma dos matrices pasadas como parametros devolviendo el resultado en 
	otra matriz }
procedure suma_matrices(matA, matB:tmatriz; var matResult:tmatriz; fil,col:integer);
var cont1, cont2:integer;
begin
	cont1:=1;
	while (cont1<=col) do
	begin
		cont2:=1;
		while (cont2<=fil) do
		begin
			matResult[cont2][cont1] := matA[cont2][cont1]+matB[cont2][cont1];
			cont2:=cont2+1;
		end;
		cont1:=cont1+1;
	end;
end;

begin
	read(fil); { introd. el numero de filas }
	read(col); { introd. el num. de columnas }
	intro_matriz(matA, fil, col);	{ introducimos matriz A }
	intro_matriz(matB, fil, col); 	{ introd. mat. B }
	suma_matrices(matA, matB, matResult, fil, col); { sumamos mat. A y B }
	mostrar_matriz(matResult, fil, col); { mostramos resultado en pantalla }
end.
