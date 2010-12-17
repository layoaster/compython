program Recoleccion;

	procedure prueba;

		{ MODO DE USO:
			 El programa queda esperando a que el usuario introduzca dos números(a y b).
		  A continuación el programa muestra operaciones realizadas con a y b:
		  a+b
		  a-b
		  a*b
		  a/b

		}
		{ Autor: M¦ Angela M‚ndez Plasencia.}
		{ Fecha: 13.10.1997.}
		{ Comentario: Programa que realiza operaciones aritm‚ticas con las variables
						  enteras x, a y b.
						  Se insertan sentencias sencillas como por ejemplo, sentencia
						  if..then, if..then..else, while..do, etc.
		  FINALIDAD: Aprender el lenguaje del Pascal- y advertir las diferencias de
						 este compilador con respecto al compilador del TP7.0.}

		const
			  Y = 2;
		{type
			 Pruueba = integer;}

		var
			 x : integer;
			 a : integer;
			 b : integer;

		procedure Comprobacion (aa, bb : integer; var xx : integer);
		{ No hace nada en especial.}
		begin
			  if (aa < bb) then
				  xx := bb - aa
			  else
					xx := aa - bb;
		end;

		{function Comprobacion2 (aa, bb : integer;): integer;
		{ Funci¢n que no realiza ninguna tarea espec¡fica, s¢lo se utiliza para
		  comprobar que el compilador toma perfectamente estas sentencias.}
		begin
			  if aa <> 1 then
				  bb := 2;
			  while (a >= b) do
				 bb := bb + bb;
			  Comprobacion2 := bb;
		end; }

	begin
		 read(a);
		 read(b);
		 x := (a + b);
		 write(x);
		 x := (a - b);
		 write(x);
		 x := (a * b);
		 write(x);
		 x := a div b;
		 write(x);
	end;

{****************************************************************}

	{
	14-10-97
	Jos‚ Gil Marichal Hern ndez
	Programa ejemplo para el punto 1.2 de la pr ctica 0 de Introducci¢n a los
	compiladores, se trata de un peque¤o programa en pascal- que comprueba que
	los programas p-c.exe (compilador pascal-) y interpre.exe (interprete del c¢_
	digo objeto) funcionan correctamente. Se trata de una implementaci¢n de una
	ordenaci¢n por burbuja muy ineficiente, pero que toca distintos aspectos del
	pascal-, como son las constantes, arrays, bucles while y sentencias if. Faltan
	sin embargo el uso de booleans y procedimientos entre otros.

	ENTRADA : se introducen por teclado los n=5 valores enteros con signo a ordenar.
	RESULTADO : a continuaci¢n se listan ordenados.
	}

	procedure p;

		const n = 5;                        {no. de el. a ordenar}

		type vector = array [1..n] of integer;

		var a : vector;                     {vector a ordenar}
			 i, j, k, inter : integer;       {¡ndices en la ordenaci¢n}

		begin
			i := 1;
			while (i <= n) do
			begin
				 read (a[i]);                 {adquisici¢n de valores via teclado}
				 i := i + 1;
			end;

			i := 1 ;
			while ( i < n ) do               {ordenaci¢n -> muy simple}
			begin
				 j := i+1;
				 k := i;
				 while (j <= n) do
				 begin
					 if (a[j]<a[k]) then
						 k := j;
					 j:=j+1;
				 end;
				 inter := a[i];
				 a[i] := a[k];
				 a[k] := inter;
				 i := i + 1;
			end;

			i := 1;
			while (i <= n) do
			begin
				write (a[i]);                 {salida por pantalla una vez ordenado}
				i := i + 1;
			end;
		end;

{****************************************************************}

	{Programa para calcular combinaciones }
	{ Following this formula: N!/(P!(N-P)!)}

	 procedure Combinacion;
		var
			N:integer;
			P:integer;
			C:integer;
			i,j:integer;

		procedure Combi(var C:integer; N:integer; P:integer);
		var
			producto1:integer;
			producto2:integer;

		begin
		  {Para evitar los calculos, utiliza la propriedad siguiente de la factorial:}
		  {A!/B! = A*(A-1)*(A-2)*...*(B+1) c¢n A>B}
			if (P>(N-P)) then
			begin
				producto2:=1; producto1:=P+1;
				i:=2;
				while (i<=(N-P)) do
				begin
					producto1:=producto1*(i+P);
					producto2:=producto2*i;
					i:=i+1;
				end;
			end
			else
			begin
				producto2:=1; producto1:=N-P+1;
				i:=2;
				while (i<=P) do
				begin
					producto1:=producto1*(i+N-P);
					producto2:=producto2*i;
					i:=i+1;
				end;
			end;
			C:=producto1 div producto2;
		end;

		{Programa Principal}
	begin
	  read(N);
	  read(P);
	  while (P > N) do {P se debe de ser superior a N}
	  begin
		  read(P);
	  end;
	  Combi(C,N,P);
	  write (C);
	end;

{****************************************************************}

	{*********************************************************}
	{ Pr cticas de Introducci¢n a los Compiladores            }
	{ Pr ctica 00                                             }
	{ COMPLEJO.P                                              }
	{ Autor: Pere Moreo Mart¡nez.                             }
	{ Fecha: 13/10/97                                         }
	{                                                         }
	{ Programa para PASCAL- con cierta dificultad.            }
	{ El programa realiza la divisi¢n real, mostrando el re-  }
	{ sultado en columna, donde la primera l¡nea es la parte  }
	{ entera y el resto de la columna, los decimales.         }
	{                                                         }
	{ Entrada: Como no se pueden presentar mensajes por panta-}
	{ lla, al arrancar el programa unicamente aparece el cur- }
	{ sor parpadeando a la espera de la introducci¢n del DIVI-}
	{ DENDO, al pulsar retorno de carro, hay que introducir el}
	{ DIVISOR. Tras pulsar retorno de carro, aparece el resul-}
	{ tado de la operaci¢n: primero la parte entera de la ope-}
	{ raci¢n (si es negativo con su signo), y en columna, los }
	{ decimales.                                              }
	{*********************************************************}

	procedure prueba1;

		const
		  max_decimales = 15;

		var
		  dividendo, divisor, cociente, resto : integer;
		  i : integer;

		begin

		{ leemos los n£meros a operar }
		  { dividendo }
		  read(dividendo);
		  { divisor }
		  read(divisor);

		  { inicializamos el contador de decimales y el resto }
		  { para poder entrar en el bucle}
		  i := 0;
		  resto := 1;

		  while (i <= max_decimales) and (resto <> 0) do
		  begin
			 cociente := dividendo div divisor;      { dividimos y obtenemos cociente }
			 resto := dividendo - cociente*divisor;  { operamos para obtener el resto }
			 write(cociente);                        { mostramos el resultado }
			 i := i + 1;                             { siguiente decimal }
			 dividendo := resto * 10;                { corregimos el valor }
			 if dividendo < 0 then                   { control de signo }
				dividendo := -1 * dividendo;
			 if divisor < 0 then
				divisor :=  -1 * divisor;
		  end;

		end;

{****************************************************************}

  {***************************************************************************
		Realiza una serie de c lculos num‚ricos. Las funciones son las
		siguientes:

		1: Halla el MCD de dos n£meros.
		Se introducen los dos n£meros y devuelve el resultado.
		Acaba el programa.
		2: Halla la  combinatoria de dos n£meros.
		Se introducen los dos n£meros y devuelve el resultado.
		Acaba el programa.
		0: Sale del programa.

		En otro caso escribe un cero por pantalla.
  ***************************************************************************}

  procedure ejemplo;

		var opcion: integer;         { las opciones del programa }
			 resultado: integer;      { es el resultado de las operaciones }
			 salir: boolean;          { para salir del programa }

			 {------------------------------------------------------------------}
			 { Calcula el MCD de 2 n£meros, poni‚ndolo en la variable resultado }
			 {------------------------------------------------------------------}

			 procedure MaxComDivisor;
			 var  n1, n2: integer;    { los n§ a los que calcular el MCD }
			 resto: integer;
			 begin
			 read (n1);
			 read (n2);
			 while n2 <> 0 do
					begin
					resto := n1 mod n2;
					n1 := n2;
					n2 := resto;
					end;
			 resultado := n1;
			 end;

			 {------------------------------------------------------------------}
			 { Pone la combinatoria de 2 n§ en la variable resultado.           }
			 {------------------------------------------------------------------}

			 procedure Combinatoria;
			 var  n1, n2: integer;       { los n§ a los que calcular la combinatoria }
			 f_1, f_2: integer;     { los factoriales del 1 y 2§ n§ }
			 temp: integer;         { variable temporal }


			{--------------------------------------------------------------}
			{ Pone el factorial de un n§ en la variable "fact".            }
			{--------------------------------------------------------------}

			procedure Factorial (n: integer; var r: integer);
			var temp: integer;      { variables temporales }
			begin
				if n = 1 then
					r := 1
				else
					begin
						n := n - 1;
						Factorial (n, temp);
						r := (n + 1) * temp;
					end;
			end;

			 begin
			read (n1);
			read (n2);
			if n1 < n2 then         { corregir posibles errores }
					begin
					temp := n1;
					n1 := n2;
					n2 := temp;
					end;

			Factorial (n2, f_2);         { factorial del 2 n§ }

			temp := n1 - n2;
			Factorial (temp, f_1);

			temp := f_2 * f_1;

			Factorial (n1, f_1);         { factorial del 1 n§ }
			resultado := f_1 div temp;
			 end;

	BEGIN
		 salir := FALSE;
		 while (not salir) do
		 begin
				write (0);                { indica el comienzo del men£ }
				read (opcion);            { lee la opci¢n del men£ }
				if opcion = 1 then
				begin
				MaxComDivisor;
				write (resultado);
				end
				else
				if opcion = 2 then
				begin
					  Combinatoria;
					  write (resultado);
				end
				else
				if opcion = 0 then
					  salir := TRUE;
		 end;
	END;

{****************************************************************}

	{*
	** 	PI.P 	Programa para calcular un determinado n§ de cifras de PI
	**     ******
	**		Autor: Juan Miguel Alvarez Tosco	Fecha: 13-10-97
	**		Objetivo: Comprobar el compilador e int‚rprete de Pascal- con
	**			  un ejemplo pr ctico.
	**		Funcionamiento: El programa solicita un n§ de d¡gitos a calcular
	**				y muestra en pantalla la lista de d¡gitos.
	**					Ojo: No incluye coma decimal
	**
	**		Nota: Algoritmo propuesto por Damir Dzeko (ddzeko@xems.fer.hr)
	**		      fecha: 1-10-96, que he traducido a Pascal-.
	*}
	procedure calcular_pi;

		const
			n_max_digitos = 30;
			n_max_restos = 100;

		type
			t_serie_digitos = array [0 .. n_max_digitos] of integer;
			t_serie_restos = array [0 .. n_max_restos] of integer;

		var
			n_digitos : integer;	   { N§ de Digitos a calcular }
				  n_restos : integer;        { N§ de Restos }
			digitos : t_serie_digitos; { Almacena las cifras decimales del n§ PI }
			restos : t_serie_restos; { Almacena los restos temporales para el calculo }
			ultimo_digito : integer; 	{ Ultimo d¡gito calculado }
			salir : boolean;	   	{ Flag para detener bucles }
			temp : integer;
			i, j, k : integer;

			procedure imprimir_serie (s_digitos : t_serie_digitos; n : integer);
			{** Imprime los digitos del n£mero por pantalla **}
			var
				i : integer;
			begin
				i := 0;
				while (i < n) do
				begin
					write(s_digitos[i]);
					i := i + 1
				end
			end;

		begin
			read(n_digitos);
			if (n_digitos < n_max_digitos) then
				n_restos := 10 * n_digitos div 3
			else
				begin
					n_digitos := n_max_digitos;
					n_restos := n_max_restos
				end;
			i := 0;
			while (i < n_restos) do		{ Inicializa el array de restos }
			begin
				restos[i] := 2;
				i := i + 1
			end;
			j := 0;
			while (j < n_digitos) do
			begin
				ultimo_digito := 0;
				i := n_restos - 1;
				while (i >= 0) do
				begin
					temp := 10 * restos[i] + ultimo_digito * (i + 1);
					restos[i] := temp mod (2 * i + 1);
					ultimo_digito := temp div (2 * i + 1);
					i := i - 1
				end;
				restos[0] := ultimo_digito mod 10;
				ultimo_digito := ultimo_digito div 10;
				if (ultimo_digito = 10) then
				begin
					ultimo_digito := 0;
					k := 1;
					salir := false;
					while ((k < j) and (not salir)) do
					begin
						digitos[j - k] := digitos[j - k] + 1;
						if (digitos[j - k] <= 9) then
							salir := true
						else
							digitos[j - k] := digitos[j - k] - 10;
						k := k + 1
					end
				end;
				digitos[j] := ultimo_digito;
				j := j + 1
			end;
			imprimir_serie(digitos, n_digitos)
		end;

{****************************************************************}


		{ Autor  : Emmanuel CORDENTE
		  Fecha  : Octubre 1997


		Este programo calcula una cifras x a la potencia n
		  Cuando n esta par el hace x^n=(x^(n/2)^2)
					n esta impar  x^n=x*x^(n-1)
		 Este Algorytmo permite de calcular potencia de x
		 con mucho menos operaciones
		}


	procedure puissance;
		var
		x,
		n       :       integer;



		procedure lit(var x,n: integer);  { Lee las variables }
		begin
		read(x);
		read(n);
		end;


		procedure puissance(var x:integer;n:integer);    { Calcula x^n }
		var                                              { Y saca el resultato en X }
		drap    :       boolean;
		tmp     :       integer;

		begin
		drap:=false;
		if n=0 then          { x^0=1 }
					  begin
					  X:=1;
					  drap:= true;
					  end;

		if (n=1) and (not drap) then     { X^1=1 }
					  drap:=true;



		if ((n mod 2)=0) and (not drap) then       { si par }
										begin
										puissance(x,n div 2);   { x^(n/2) }
										x:=x*x;                 { X^2 }
										drap:=true;
										end;

		if ((n mod 2)=1) and (not drap) then       { si inpar }
										begin
										tmp:=x;
										puissance(x,n-1);       { x^(n-1) }
										x:=tmp*x;
										end;
		end;


		begin
		lit(X,N);
		puissance(x,n);
		write(x);
	end;

{***********************************************************************}

		{ Programa para probar el uso de registro. El programa NO ES EFICIENTE, pero
		prueba diversos aspectos de los registros: pasa por valor y variable, acceso
		a campos, etc....

		MODO DE USO: Primero se introduce el numero de coordenadas, y luego el valor,
		para cada una de ellas (se separa cada vector por -1111). Luego indica el
		resultado del producto escalar y cuantos puntos de los vectores estan sobre
		algun eje.

		AUTOR: Antonio Javier Dorta Lorenzo	(alu1848)}


		procedure prod_esc;

		const
			max = 100;

		type
			tipo_vect = record
								i, j : integer;
								eje1, eje2 : boolean;
								resultado : integer
							end;
			vectores = array [1..max] of tipo_vect;

		var n, i : integer;
			a, b, c : vectores;
			resultado, eje : integer;

			procedure tomar_datos (var r : tipo_vect);

			begin
				read (r.i);
				read (r.j);
				if ((r.i = 0) or (r.j = 0)) then
					r.eje1 := TRUE
				else
					r.eje1 := FALSE
			end;


			procedure calc_prod_escalar (var r_out : tipo_vect; r1, r2 : tipo_vect);

			begin
				r_out.resultado := (r1.i * r2.i) + (r1.j * r2.j);
				if r1.eje1 then
					r_out.eje1 := TRUE
				else
					r_out.eje1 := FALSE;
				if r2.eje1 then
					r_out.eje2 := TRUE
				else
					r_out.eje2 := FALSE;
			end;

		begin
			read (n);
			if n <= max then
			begin
				i := 1;
				while i <= n do
				begin
					tomar_datos (a[i]);
					i := i + 1;
				end;
				i := 1;
				while i <= n do
				begin
					tomar_datos (b[i]);
					calc_prod_escalar (c[i], a[i], b[i]);
					i := i + 1;
				end;
				resultado := 0;
				eje := 0;
				i := 1;
				while i <= n do
				begin
					resultado := resultado + c[i].resultado;
					if c[i].eje1 then
						eje := eje + 1;
					if c[i].eje2 then
						eje := eje + 1;
					i := i + 1;
				end;
				write (-1111);
				write (resultado);
				write (eje);
			end;
		end;

{**************************************************************************}

		procedure qsort;  { Programa que realiza ordenacion por metodo quicksort }

		CONST
			Nmax = 8;                    { Numero maximo de elemento ha ordenar }

		TYPE
			cadena = ARRAY [1..8] OF integer;          { Tipo cadena de enteros }

		VAR
			vector : cadena;                      { Vector de enteros a ordenar }
			cont   : integer;                               { Contador auxiliar }

			procedure quicksort(iz, de : integer);      { Proced. de Ordenacion }
			VAR i, j  : integer;                           { Indices del vector }
				 media : integer;                    { Posicion media del vector }
				 reg   : integer;                            { registro auxiliar }

			begin
				i := iz;                     { indice izquierda = limite inferior }
				j := de;                       { indice derecha = limite superior }
				media := vector[((iz + de) div 2)];        { halla posici¢n media }

				while (vector[i] < media) do     { Inc. i mientras menor que media }
					i := i + 1;

				while (media < vector[j]) do     { Dec. j mientras mayor que media }
					j := j - 1;

				if (i <= j) then                             { Si j sobrepasa a i }
				begin
					reg := vector[i];                { Guardamos pos. i del vector }
					vector[i] := vector[j]; { Intercambia valores index. por i y j }
					vector[j] := reg;                           { Actualiza pos. j }
					i := i + 1;                                    { Inc. indice i }
					j := j - 1;                                    { Inc. indice j }
				end;

				while (i <= j) do      { => indice i este por debajo del indice j }
				begin
					while (vector[i] < media) do { Inc. i mientras menor que media }
						i := i + 1;

					while (media < vector[j]) do { Dec. j mientras mayor que media }
						j := j - 1;

					if (i <= j) then                         { Si j sobrepasa a i }
					begin
						reg := vector[i];            { Guardamos pos. i del vector }
						vector[i] := vector[j];  { Inter. valores index. por i y j }
						vector[j] := reg;                       { Actualiza pos. j }
						i := i + 1;                                { Inc. indice i }
						j := j - 1;                                { Inc. indice j }
					end;
				end;

				if (iz < j) then quicksort(iz, j);    { llama funcion quick sort con nuevos limites de vector }
				if (i < de) then quicksort(i, de);    { llama funcion quick sort con nuevos limites de vector }
			end;

		BEGIN
			cont := Nmax;                                  { inicializa contador }
			while (cont >= 1) do                          { inicializamos vector }
			begin
				vector[(Nmax - cont + 1)] := cont;
				write(cont);
				cont := cont - 1;
			end;
			quicksort(1, Nmax);                                  { ordena vector }
			cont := 1;
			while (cont <= Nmax) do                       { muestra vector ordenado }
			begin
				write(vector[cont]);
				cont := cont + 1;
			end;
		END;

{************************************************************************}

	  { ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
		Autor : Rom n Sosa Gonz lez
		Finalidad: calcular determinantes de hasta 10*10
		Modo de uso:
			  Se pide el rango (¨se llama as¡?) del determinante.
			  Luego se van pidiendo las componentes de la matriz,
				 pidiendo [1,1], [1,2], [1,3]... [1,n] ->
						->  [2,1], [2,2], .....    [2,n] ->
							 ...
						->  [n,1], [n,2], ....     [n,n]

			  El £ltimo n§ que aparece ser¡a el valor del determinante.

		 No est  probado para Pascal-

	  ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ }

	  {Un determinante de rango 10 tarda como un minuto...}
	  procedure Hallar_determinante;

	  const nmax = 10;  {rango max de un determinante}
			  nmin = 2;   {rango min de un determinante}

	  type
			tabla0_t= array[1..nmax] of integer;
			tabla_t=array[1..nmax] of tabla0_t;


	  var i, j, grado: integer;
			tabla: tabla_t;
			res: integer;

			{halla el subdeterminante quitando la fila n y la columna i}
	  procedure hallar_subtabla (var aux:tabla_t; tabla:tabla_t; i,n:integer);
	  var j,k:integer;
	  begin
			j:= 1;
			while (j <= n-1) do
			begin
				 k:= 1;
				 while k <= i-1 do
				 begin
					  aux[j][k]:= tabla[j][k];
					  k := k+1;
				 end;
				 k := i+1;
				 while k <= n do
				 begin
					  aux[j][k-1]:= tabla[j][k];
					  k:= k+1;
				 end;
				 j:= j+1;
			end;
	  end;

	  procedure det (tabla:tabla_t; n:integer; var res: integer);
	  var aux, aux2:integer;
			subtabla:tabla_t;
			i:integer;
	  begin
			if n = 2
			then res:= tabla[1][1]*tabla[2][2] - tabla[2][1]*tabla[1][2]
			else
			  begin
				 aux:= 0;
				 i:= 1;
				 while i <= n do      { desarrolla respecto a la última fila }
				 begin
					 hallar_subtabla (subtabla, tabla, i,n);
					 if (n+i) mod 2 = 0
						 {averigua el signo dl subdeterminante}
					 then begin
						 det(subtabla, n-1, aux2);
						 aux:= aux + tabla[n][i] * aux2;
					 end
					 else begin
						 det(subtabla, n-1, aux2);
						 aux:= aux - tabla[n][i] * aux2;
					 end;
					 i:= i+1;
				 end;
				 res:= aux;
			  end;
	  end;


  begin
		read (grado);
		if not( (grado > nmax) or (grado < nmin) )
		then begin
		  i:= 1;
		  while i <= grado do
		  begin
			  j:= 1;
			  while j <= grado do
			  begin
				 read (tabla[i][j]);
				 write (tabla[i][j]);
				 j:= j+1;
			 end;
			 i:= i+1;
		  end;
		  det (tabla, grado, res);

		  write (res);
		end;
  end;

{*************************************************************************}
		{
			 Alumno: Fernando Arvelo Rosales. (alu1661).

			 Raiz:
				  Este programa ha sido desarrollado en el lenguage Pascal- para
			 comprobar el funcionamiento del compilador y del interprete que
			 nos han dado como ejemplo.

			 Descripci¢n:
				  El programa espera la introducci¢n de un numero y calcula su
			 raiz cuadrada. Utiliza un metodo iterativo que se basa en la siguiente
			 afirmaci¢n:

				  Sea A una aproximaci¢n a la raiz cuadrada de X.
				  entonces B = (X/A + A)/2 es una mejor aproximaci¢n.

			 Nota:
				  La raiz se calcular  con una aproximaci¢n de ( +1 | -1 )

		}

		procedure raiz;

		var
			 x, a, a_anterior : INTEGER;

			 procedure calcula_raiz (var a: integer; x: integer);
			 var
				  aux : integer;
			 begin
				  aux := x div a;
				  aux := aux + a;
				  a := aux div 2;
			 end;

		BEGIN
			 read (x);

			 if x = 0 then
				  write (0)
			 else if x > 0 then
			 begin
				  a_anterior := x;
				  a := x;

				  calcula_raiz (a, x);

				  while (a_anterior - a) > 1 do
				  begin
						a_anterior := a;
						calcula_raiz (a, x);
				  end;
				  write (a);
			 end
		END;

begin
	prueba;
	p;
	prueba1;
	Combinacion;
	ejemplo;
	calcular_pi;
	puissance;
	prod_esc;
	Hallar_determinante;
	qsort;
	raiz;
end.
