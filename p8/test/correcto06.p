{*****************************************************************************
PROGRAMA : Practica nº1 de Compiladores (Implementacion de un programa en p-)
AUTOR	   : Miguel Angel Delgado Gonzalez
FECHA	   : 19/10/00
FINALIDAD: Implementación del algoritmo de coloracion minima de un grafo,
			  haciendo uso de la tecnica de ramificacion y acotación.
			  Por tanto dado un grafo de entrada, la finalidad del programa es
			  determinar el numero de colores minimo necesarios para colorear
			  cada uno de los nodos del grafo de forma que dos nodos adyacentes
			  no tengan el mismo color.

			  Datos de entrada:
					Los datos de entrada que recibirá el programa son, el numero de
					vertices del grafo, seguido del número de aristas definidas, y
					a continuacion para cada una de las aristas se definiran sus
					extremos. Estos datos se leeran a traves de teclado con el
					formato:
									numeroVertices
									numeroAristas
									verticeInicial1   verticeFinal1
									.....					......

			Datos de salida:
					El programa mostrara al final el numero minimo de colores
					necesarios para colorear el grafo y el color que se asigna
					a cada uno de los nodos o vertices del grafo.
			Ejemplo:
					Supongamos que el grafo de entrada posee 4 nodos y 4 aristas,
					y se existen las conexiones entre vertices:

									1 -------- 2
                           |          |
									|          |
									|          |
									3----------4
					La entrada del programa para este grafo deberia  ser:
					4
					4
					1 2
					1 3
					2 4
					3 4
					Y su correspondiente salida es:
									21221
					El primer digito indica el numero de colores, mientras el resto
					indica el numero de color de cada uno de los elementos del vector

HISTORIA:
******************************************************************************}
program pract01_Compi;
const
	MAXNODOS = 10;
type
	vNodos = array [1..MAXNODOS] of integer;
	listaAdyacencia = array [1..MAXNODOS] of vNodos;
	vectBooleano = array [1..MAXNODOS] of boolean;
var
	vectNumAd,					{ vector con el computo de adyacencias }
	vectSol,						{ vector de solucion parcial }
	vectSolOptimo : vNodos; { vector con la solucion optima }
	lA : listaAdyacencia;   { lista de adyacencia }
	nNodos, 						{ nº de nodos totales del grafo }
	optimo : integer;       { nº de colores de la solucion optima }

{*******************************************************************************
PROCEDIMIENTO: copiarVect
FINALIDAD	 : Copia un vector origen en un vector destino. Se utiliza cuando
					una solución parcial es mejor que la total obtenida hasta el
					momento. Entonces tiene lugar la copia de los vectores.
*******************************************************************************}
procedure copiarVect(var vectSolOptimo : vNodos; vectSol : vNodos);
	var
		i : integer;
	begin
		i := 1;
		while (i <= nNodos) do
			begin
				vectSolOptimo[i] := vectSol[i];
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: inicializa
FINALIDAD	 : Lleva a cabo la inicializacion de los vectores que almacenan
					los resultados del programa, tanto de las soluciones parciales,
					como de la global.
*******************************************************************************}
procedure inicializa(var vectSol : vNodos; var vectSolOptimo : vNodos; 
							var vectNumAd : vNodos);
	var
		i : integer;
	begin
		i := 1;
		while (i <= MAXNODOS) do
			begin
				vectNumAd[i] := 0;
				vectSol[i] := 0;
				vectSolOptimo[i] := i;
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: cargarLista
FINALIDAD	 : Lee desde el terminal el numero de nodos, aristas, y cada uno
					de los vertices de las aristas hasta que el grafo quede definido.
					Es en este procedimiento donde se crea la lista de adyacencia.
					Al ser la direccion de las aristas de los vertices irrelevante
					para la coloracion, el la lista de adyacencia, por cada entrada
					de una arista se modifican las listas del origen y extremo.
*******************************************************************************}
procedure cargarLista(var lA : listaAdyacencia; var vectNumAd : vNodos; 
						   var nNodos : integer; var optimo : integer);
	var
		nAristas, aux, i : integer;
		origen, destino : integer;
	begin
		read(nNodos);			{ nº de nodos del grafo }
		read(nAristas);		{ nº de aristas }
		optimo := nNodos;
		i := 1;
		while (i <= nAristas) do
			begin
				read(origen);
				read(destino);
				{ Insertamos el destino en la lista de Adyacencia del origen }
				vectNumAd[origen] := vectNumAd[origen] + 1;
				aux := vectNumAd[origen];
				lA[origen][aux] := destino;
				{ Insertamos el origen en la lista de Adyacencia del destino }
				vectNumAd[destino] := vectNumAd[destino] + 1;
				aux := vectNumAd[destino];
				lA[destino][aux] := origen;
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: calculoNumColores
FINALIDAD	 : recorre el vector que almacena los colores correspondientes a
					cada vertice del grafo y determina el número de colores que
					son precisos para la coloración del grafo.
*******************************************************************************}
procedure calculoNumColores(var numCol : integer; v : vNodos; num : integer);
	var
		i, colAct : integer;		 { var. auxiliares }
		utilizado : vectBooleano;{ vector booleano de marcas para el computo }
	begin
		numCol := 0;
		i := 1;
		while (i <= nNodos) do  { Inicializamos a FALSE el vector de marcas }
			begin
				utilizado[i] := FALSE;
				i := i + 1;
			end;
		i := 1;
		while (i <= num) do { Realizamos el computo de colores }
			begin
				colAct := v[i];
				if (not utilizado[colAct]) then
					begin
						numCol := numCol + 1;
						utilizado[colAct] := TRUE;
					end;
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: mostrarSolucion
FINALIDAD	 : Muestra el número minimo de colores que son precisos para la
					minima coloracion, asi como el color correspondienta a cada nodo
*******************************************************************************}
procedure mostrarSolucion(vectSolOptimo : vNodos; nNodos : integer);
	var
		i, numColores : integer;
	begin
		calculoNumColores(numColores, vectSolOptimo, nNodos);
		write(numColores);
		i := 1;
		while (i <= nNodos) do
			begin
				write(vectSolOptimo[i]);
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: solucionValida
FINALIDAD	 : Modifica la variable booleanna esSolucion, pasada por variable
					al procedimiento, con un valor TRUE si al nodo considerado
					actualmente se le puede asignar el color actual, esto es , la
					variable esSolucion tomara el valor TRUE si ninguno de los nodos
					adyacentes al actual posee el color actual.
					En caso de que alguno de los nodos adyacentes ya posea dicho
					color, la variable esSolucion tomará el valor FALSE
*******************************************************************************}
procedure solucionValida(lA : listaAdyacencia; nodoActual : integer; 
					vectNumAd : vNodos; vectSol : vNodos; var esSolucion : boolean);
	var
		i, color, numNodos, p : integer;
	begin
		esSolucion := TRUE;
		color := vectSol[nodoActual];	{ color asignado al nodo actual }
		numNodos := vectNumAd[nodoActual];
		i := 1;
		while (i <= numNodos) and (esSolucion) do { recorremos su lA }
			begin
				p := lA[nodoActual][i];
				if (vectSol[p] = color) then
					esSolucion := FALSE;
				i := i + 1;
			end;
	end;

{*******************************************************************************
PROCEDIMIENTO: minKcoloracion
FINALIDAD	 : Procedimiento que lleva a cabo la minima coloracion del grafo.
					Se implementa la tecnica recursiva de ramificaci¢n y acotaci¢n,
					por lo que el procedimiento genera varias soluciones parciales.
					De entre todas las soluciones parciales generadas, se
					selecciona aquella que posea mejor bondad, esto es, aquella en
					la que el n£mero de colores resulte minimo.
*******************************************************************************}
procedure minKcoloracion(lA : listaAdyacencia; nodo : integer; 
								 var vectSol : vNodos; var vectSolOptimo : vNodos);
	var
		i, aux 	  : integer;
		esSolucion : boolean;
	begin
		i := 1;
		while (i < optimo) do
			begin
				vectSol[nodo] := i; { Se selecciona un nuevo color, ¨ Es valido ? }
				solucionValida(lA, nodo, vectNumAd, vectSol, esSolucion);
				calculoNumColores(aux, vectSol, nodo);
				if (esSolucion)  and (aux < optimo) then
					if (nodo = nNodos) then
						begin { Se almacena la solucion parcial con mayor bondad }
							calculoNumColores(optimo, vectSol, nodo);
							copiarVect(vectSolOptimo, vectSol);
						end
					else 		{ Establecemos el color del siguiente nodo }
						minKcoloracion(lA, nodo + 1, vectSol, vectSolOptimo);
				i := i + 1;
			end;
	end;

{******************************************************************************}
begin
	inicializa(vectSol, vectSolOptimo, vectNumAd);
	cargarLista(lA, vectNumAd, nNodos, optimo);
	minKcoloracion(lA, 1, vectSol, vectSolOptimo);
	mostrarSolucion(vectSolOptimo, nNodos);
end.


















