{****************************************************************************
* AUTOR: Juan Ram¢n Gonz†lez Gonz†lez
* PRACTICA 1: Introducci¢n al lenguaje Pascal-
* DESCRIPCI‡N: Programa en Pascal- que permite multiplicar 2 matrices cuadra-
*              das de dimensi¢n N * N (N fijado en el c¢digo).
* ASIGNATURA: Introducci¢n a los Compiladores I
* ULTIMA MODIFICACI‡N: 18-10-2000
* MODO DE USO:
*    -La constante N fija la dimensi¢n de las matrices a N * N.
*    -Introducir la primera matriz por filas.
*    -Introducir la segunda matriz por filas.
*    -Se obtiene la matriz producto tambiÇn por filas.
****************************************************************************}
program mult_mat;

const N = 2;

type
	Fila = array[1..N] of integer;
	Matrices = array[1..N] of Fila;

var
	matrizA : Matrices;
	matrizB : Matrices;
	matrizRes : Matrices;

{****************************************************************************
* LeerMatriz -- Lee una matriz por filas.
****************************************************************************}
procedure LeerMatriz(var matriz : Matrices);
var
	i, j: integer;

begin
	i := 1;
	while (i <= N) do
	begin
		j := 1;
		while (j <= N) do
		begin
			read(matriz[i][j]);
			j := j + 1;
		end;
		i := i + 1;
	end
end;

{****************************************************************************
* MultiplicarMatrices -- Multiplica matrizA por matrizB, devolviendo en
* matrizRes el resultado de dicha operaci¢n.
****************************************************************************}
procedure MultiplicarMatrices(matrizA, matrizB : Matrices;
                              var matrizRes : Matrices);
var
	i, j, k : integer;

begin
	i := 1;
	while (i <= N) do
	begin
		j := 1;
		while (j <= N) do
		begin
			k := 1;
			matrizRes[i][j] := 0;
			while (k <= N) do
			begin
				{---------------------------------------------------------------
				| El elemento de la matriz producto en la fila i y columna j es
				| el resultado de sumar los productos de los elementos de la
				| fila i de la matrizA por los de la columna j de la matrizB.
				 ---------------------------------------------------------------}
				matrizRes[i][j] := matrizRes[i][j] +
										 matrizA[i][k] * matrizB[k][j];
				k := k + 1;
			end;
			j := j + 1;
		end;
		i := i + 1;
	end;
end;

{****************************************************************************
* MostrarMatriz -- Muestra una matriz por filas.
****************************************************************************}
procedure MostrarMatriz(matriz : Matrices);
var
	i, j : integer;

begin
	i := 1;
	while (i <= N) do
	begin
		j := 1;
		while (j <= N) do
		begin
			write(matriz[i][j]);
			j := j + 1;
		end;
		i := i + 1;
	end;
end;

begin
	LeerMatriz(matrizA);
	LeerMatriz(matrizB);
	MultiplicarMatrices(matrizA, matrizB, matrizRes);
	MostrarMatriz(matrizRes);
end.

