Program determinante;
{ Centro Superior de Inform tica. Curso 2000/20001.
  Introduccion a los compiladores I.

  Practica 1: Introduccion al Pascal-.

  AUTOR: Carlos Merino Gracia.

  Objetivo: El objetivo de la practica es probar la funcionalidad del
	compilador de Pascal- realizado en a¤os anteriores en la asignatura.
	Para ello se implementara una funcion de calculo del determinante de una
	matriz por el metodo de los adjuntos.
}

{ Comentarios anidados: }
{ Nivel 1: { Nivel 2: { Nivel 3: { Nivel 4: } 3 } 2 } 1 }

const 
	MAX_ELEM		= 25;			{ N£mero m ximo de elementos en el vector-matriz }

type
	{ El tipo matriz ser  un vector de elementos. Cada n elementos ser  una
	fila nueva, siendo n el orden de la matriz cuadrada. }
	Matriz = array[1..MAX_ELEM] of integer;

var
	m : matriz;					{ Matriz inicial sobre la que se trabajar  }
	n : integer;				{ Orden inicial de la matriz }
	d : integer;				{ Destino del valor del determinante }

{ ------------------------------------------------------------------------- }
{ Getij - Devuelve el elemento que ocupa la posici¢n (i,j) de la matriz
	cuadrada M de orden n. El resultado se devolver  en e. El primer
	elemento de la matriz es el (0,0), sin embargo en el vector se
	guardar n a partir del elemento 1. }
Procedure Getij(M : Matriz; n : integer; i, j : integer; var e : integer);
Begin
	e := M[i * n + j + 1];
End;

{ ------------------------------------------------------------------------- }
{ Setij - Asigna al elemento que ocupa la posici¢n (i,j) de la matriz
	cuadrada M, de orden n, el valor de e } 
Procedure Setij(Var M : Matriz; n : integer; i, j : integer; e : integer);
Begin
	M[i * n + j + 1] := e;
End;

{ ------------------------------------------------------------------------- }
{ LeerMatriz - Lee una matriz cuadrada de orden n por la entrada, pidiendo 
	uno a uno los elementos. Fila a fila. }
Procedure LeerMatriz(Var M : Matriz; n : integer);
Var
	i, j, e : integer;

Begin
	i := 0;
	while i < n do Begin
		j := 0;
		while j < n do Begin
			read(e);
			Setij(M, n, i, j, e);
			j := j + 1;
		end;
		i := i + 1;
	end;
End;

{ ------------------------------------------------------------------------- }
{ Determinante - Calcula de forma recursiva el determinante de la matriz
	cuadrada M, de orden n, por el m‚todo de los adjuntos. El m‚todo consiste,
	para un determinante de orden 3, en:
	    | a b c |
	A = | d e f | = a * | e f | - b * | d f | + c * | d e |
       | g h i |       | h i |       | g i |       | g h |
	Cada uno de los determinantes menores se calcular  llamando recursivamente
	a la rutina. El nuevo determinante se calcular  creando una nueva matriz
	con los elementos apropiados.
}
Procedure Determinante(M : Matriz; n : integer; var d : integer);
Var
	{ i, j - Indices para moverse por la matriz }
	{ k - Indice que indica el n£mero del adjunto }
	{ tmp - Variable que se encargar  de transportar los valores que resultan
		de la llamada a un procedimiento que deberia ser funci¢n. }
	i, j, k, tmp : integer;
	{ signo - Indica el signo del adjunto. Va alternando. }
	signo : integer;
	{ M2 - Nueva matriz que se genera para el c lculo del menor. }
	M2 : Matriz;

Begin
	{ * CONDICION DE PARADA: }
	{ Si el orden es 1, el determinante es el £nico elemento de la matriz. }
	if n = 1 then
		d := M[1]
	else begin
		signo := +1;
		d := 0;
		k := 0;
		{ for k := 0 to n-1 do begin }
		while k < n do begin
			i := 1;
			{ for i := 1 to n-1 do begin }
			while i < n do begin
				j := 0;
				{ for j := 0 to k-1 do begin }
				while j < k do begin
					Getij(M, n, i, j, tmp);
					Setij(M2, n - 1, i - 1, j, tmp);
					j := j + 1;
				end;
				j := k + 1;
				{ for j := k+1 to n-1 do begin }
				while j < n do begin
					Getij(M, n, i, j, tmp);
					Setij(M2, n - 1, i - 1, j - 1, tmp);
					j := j + 1;
				end;
				i := i + 1;
			end;
			Determinante(M2, n - 1, tmp);
			tmp := tmp * signo;
			d := d + tmp * M[k + 1];

			if (signo > 0) then
				signo := -1
			else
				signo := 1;

			k := k + 1;
		end;
	end;
End;

{ ------------------------------------------------------------------------- }
{ Programa principal. El comportamiento del programa ser  el siguiente:
	- Recoger  en primer lugar un n£mero. Ser  el orden de la matriz.
	- A continuaci¢n recoger  n * n valores que ir  colocando en la matriz,
	fila a fila. 
	- Por £ltimo devolver  un valor que corresponder  al determinante de la
	matriz.
	- En caso de error al introducir el orden de la matriz (muy grande o muy
	peque¤o), escribir  dos -1, que es imposible que sean una salida normal
	del programa.
}
Begin
	{ Primer paso: Leer el orden de la matriz. }
	read(n);

	{ Comprobar que el orden de la matriz sea apropiado. }
	if (n*n > MAX_ELEM) or (n*n < 1) then begin
		{ Escribir un c¢digo de error... }
		write(-1);
		write(-1);
	end else begin
		LeerMatriz(M, n);
		Determinante(M, n, d);
		write(d);
	end;
End.

