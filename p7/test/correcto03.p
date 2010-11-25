{****************************************************************************** 
 PROGRAMA: trasp_matriz.
 AUTOR: Isaac Jonathan Delgado Nunez. (alu2234@csi.ull.es)
 ASIGNATURA: Introduccion a los Compiladores I.
 FECHA: 19-10-2000
 PRACTICA: 1.- Introduccion al lenguaje de Pascal-
 FINALIDAD: Esta practica tiene por objetivo introducir las caracteristicas ba- 
				sicas del lenguaje sobre el que se va a desarrollar un compilador. 
				Este programa servira de prueba para dicho compilador.
				El programa consiste en trasponer una matriz cuadrada por el metodo
				de "divide y venceras", el cual lo hace con un orden de complejidad
				de n*n*log2 n.
				Para abordar este problema, primeramente hay que considerar que la
				matriz sea cuadrada y potencia de 2. Esto es asi, debido a que la
				matriz se va subdiviendo en 4 matrices de orden mitad, hasta llegar
				al caso basico donde la matriz tiene orden 2 y solo hay que tras-
				poner los elementos de la diagonal secundaria. Ademas hay que per-
				mutar las submatrices 2 y 3, es decir, aquellas cuyos elementos 
				ocupan la diagonal secundaria.
							
							Caso basico n=2

							1 2 => 1 3
							3 4	 2 4 
				
							Caso general n=k (Se divide en 4 matrices de orden mitad)

							M11 M12 => M11 M21
							M21 M22 	  M12 M22
     			
				El programa solicita al principio el orden de la matriz, el cual 
				tiene que estar entre 2 y N, donde N es una constante del programa. 
				Si no se introduce un valor correcto, el programa vuelve a pregun-
				tar. Genera la matriz de forma aleatoria y va mostrando por pantalla
				los valores, debido a que no se imprime caracteres se ha tomado el
				0 por separador. Cuando acabe una linea, el programa se queda a la 
				espera de introducir un valor entero, de manera que simula un salto
				de linea.
				Por ejemplo, si proponemos una matriz de 4x4 (entrada 4), el 
				programa produce:
				Matriz generada "aleatoriamente":
            80807020
				50301090
				10701040
				80207050
				Matriz traspuesta:
				80501080
				80307020
				70101070
				20904050
				
				{ Comentarios encadenados { 1 } Comentarios encadenados } 
*******************************************************************************}
Program trasp_matriz;

const N = 16;												{ Tamano max. del vector }
      BASE = 9;											{ Base decimal }
		SEMILLA = 7;										{ Semilla para no. aleatorios }
		ORDEN_MINIMO = 2;									{ Orden minimo de la matriz }
		SEPARADOR = 0;										{ Separador de caracteres }

type vector = array [1..N] of integer;				{ Tipo del vector }
	  matriz = array [1..N] of vector;				{ Tipo de la matriz }

 
var a : matriz;											{ Matriz a trasponer }
	 orden : integer;										{ Orden de la matriz }
	 es_potencia_2 : boolean;							{ True, orden es potencia de 2 }

{******************************************************************************
 RUTINA: potencia_2.
 FUNCION: Comprueba si el valor que se le pasa por parametro es potencia de 2.
 			 Es necesario porque el algoritmo solo trabaja con matrices cuadradas y				de orden, potencia de 2. Para ello va diviendo el numero por dos hasta			  que valga 1, y si algun resto es distinto de 0, entonces no es poten-
			 cia de 2.

 PARAMETROS:
			- valor: Orden de la matriz.
			- resultado: Devuelve true o false segun sea o no potencia de 2.
******************************************************************************}
procedure potencia_2(valor : integer; var resultado : boolean);
var resto : integer;										{ Resto de la division }

begin
	resto := valor;										{ Inicializacion de vables. }
	resultado := true;									{ Consideramos potencia de 2 }
   while (valor <> 1) do
	begin
      resto := valor mod 2;
		valor := valor div 2;
      if (resto <> 0) then								{ No es potencia de 2 }
			resultado := false;
	end;
end;

{******************************************************************************
 RUTINA: generar_matriz.
 FUNCION: Funcion encargada de rellenar la matriz con valores pseudoaleatorios
			 mediante una semilla y una operacion en modulo 10 para que nos de-
			 vuelva un valor entre 1 y 9. 

 PARAMETROS:
			- m: Matriz a rellenar.
			- orden: Orden de la matriz.
******************************************************************************}
procedure generar_matriz(var m : matriz; orden : integer);
var i, j : integer;
	 valor : integer;								{ Valor del elemento de la matriz }

begin
	i := 1;
   valor := SEMILLA;								{ Inicializamos a la semilla }
   while i <= orden do
	begin
		j := 1;
      while j <= orden do
		begin
         valor := ((valor * i * j) mod BASE) + 1;  { No. aleatorio }
			m[i][j] := valor;
			j := j + 1;
		end;
		i := i + 1;
	end;
end;

{******************************************************************************
 RUTINA: mostrar_matriz.
 FUNCION: Rutina encargada de mostrar la matriz por pantalla.
 PARAMETROS:
			- m: Matriz a rellenar.
			- orden: Orden de la matriz.
******************************************************************************}
procedure mostrar_matriz(m : matriz; orden : integer);
var i, j, auxiliar : integer;

begin
	i := 1;
   while i <= orden do
	begin
		j := 1;
      while j <= orden do
		begin
         write(m[i][j]);
			write(SEPARADOR);
			j := j + 1;
		end;
      read(auxiliar);
		i := i + 1;
	end;
end;

{******************************************************************************
 RUTINA: intercambiar.
 FUNCION: Esta rutina se encarga de intercambiar las matrices M12 y M21, para 
			 ello recorre las matrices y mediante un valor auxiliar "copia" in-
			 tercambia los valores.

 PARAMETROS:
			- a, b: Matriz a intercambiar.
			- orden: Orden de la matriz.
******************************************************************************}
procedure intercambiar(var a, b : matriz; orden : integer);
var i, j, copia : integer;

begin
   i := 1;
   while i <= orden do
   begin
      j := 1;
      while j <= orden do
      begin
			copia := a[i][j];									{ Intercambio de valores }
			a[i][j] := b[i][j];
			b[i][j] := copia;
         j := j + 1;
      end;
      i := i + 1;
   end;
end;

{******************************************************************************
 RUTINA: mezclar.
 FUNCION: Esta rutina se encarga de fusionar las 4 submatrices de orden "orden" 
			 en una matriz de orden doble. Para ello se va moviendo por las
			 matrices y coloca los valores en la matriz general, simplemente 
			 moviendo los subindices.

 PARAMETROS:
			- a, b, c, d: Submatrices de orden mitad.
			- t: Matriz a devolver.
			- orden: Orden de la matriz.
******************************************************************************}
procedure mezclar(a, b, c, d : matriz; var t : matriz; orden : integer);
var i, j : integer;

begin
   i := 1;												
   while i <= (orden div 2) do
   begin
      j := 1;
      while j <= (orden div 2) do
      begin
			t[i][j] := a[i][j];												{ Matriz M11 }
		   t[i][j + (orden div 2)] := b[i][j];							{ Matriz M12 }
			t[i + (orden div 2)][j] := c[i][j];							{ Matriz M21 }
		   t[i + (orden div 2)][j + (orden div 2)] := d[i][j]; 	{ Matriz M22 }
         j := j + 1;
      end;
      i := i + 1;
   end;
end;

{******************************************************************************
 RUTINA: trasponer.
 FUNCION: Rutina principal del programa encargada de la recursividad. Distingue
			 los dos casos, el basico donde la matriz tiene orden minimo, y si no
			 es asi entonces construye 4 submatrices y se llama recursivamente. 

 PARAMETROS:
			- m: Matriz a trasponer. 
			- orden: Orden de la matriz.
******************************************************************************}
procedure trasponer(var a : matriz; orden : integer);
var u, v, w, x : matriz;							{ Submatrices M11, M12, M21, M22 }
  	 copia, i, j : integer;				

begin
	if orden = ORDEN_MINIMO then
  	begin
      copia := a[orden][1];
      a[orden][1] := a[1][orden];
      a[1][orden] := copia;
	end
	else
	begin
      i := 1;												{ Matriz M11 }
      while i <= (orden div 2) do	
      begin
         j := 1;
         while j <= (orden div 2) do
         begin
            u[i][j] := a[i][j];
            j := j + 1;
         end;
         i := i + 1;
      end;
		trasponer(u, orden div 2);

      i := 1;												{ Matriz M12 }
      while i <= (orden div 2) do
      begin
         j := (orden div 2) + 1;
         while j <= orden do
         begin
            v[i][j - (orden div 2)] := a[i][j];
            j := j + 1;
         end;
         i := i + 1;
      end;
		trasponer(v, orden div 2);

      i := (orden div 2) + 1;							{ Matriz M21 }
      while i <= orden do
      begin
         j := 1;
         while j <= (orden div 2) do
         begin
            w[i - (orden div 2)][j] := a[i][j];
            j := j + 1;
         end;
         i := i + 1;
      end;
      trasponer(w, orden div 2);

      i := (orden div 2) + 1;							{ Matriz M22 }
      while i <= orden do
      begin
         j := (orden div 2) + 1;
         while j <= orden do
         begin
            x[i - (orden div 2)][j - (orden div 2)] := a[i][j];
            j := j + 1;
         end;
         i := i + 1;
      end;
		trasponer(x, orden div 2);
      
		intercambiar(v, w, orden div 2);	{ Intercambiamos M12 - M21 }
		mezclar(u, v, w, x, a, orden);	{ Fusionamos en matriz original }
  end;
end;

{**************************** PROGRAMA PRINCIPAL *****************************}

BEGIN
   es_potencia_2 := false;
	orden := ORDEN_MINIMO;
   while (not es_potencia_2) and (orden >= ORDEN_MINIMO) do 
	begin
		read(orden);							{ Lee orden mientras sea potencia de 2 }
		potencia_2(orden, es_potencia_2);
   end; 
	generar_matriz(a, orden);
	mostrar_matriz(a, orden);
	trasponer(a, orden);
   mostrar_matriz(a, orden); 
END.
