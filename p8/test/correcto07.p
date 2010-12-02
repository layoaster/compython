 
 {*************************************************************************
 Introduccion a los Compiladores I 
 Practica 1. Introduccion al lenguaje Pascal -

	Autor: Deepak Pritamdas Daswani Daswani
	Hora: Jueves, 15:00 - 16:00 h.
	e-mail: dipupd@iic.vanaga.es, alu2232@csi.ull.es

	Finalidad: La practica consiste en realizar un pequeno programa en 
	Pascal -, con el fin de familiarizarnos con esta acotcacion del Pascal,
	asi como de probar el compilador que vamos a crear posteriormene en fu-
	turas practicas. Se trata de idear un programa en Pascal - para desenvol-
 	ernos a la hora de utilizar el lenguaje y de probar a utilizar el compi-
	lador. 
		El programa que yo he generado en esta practica resuelve el problema
	del vector minimo. Dados dos vectores X = (x1,x2,..Xn), Y = (y1,y2,..Yn)
	decimos que X < Y si existe un subindice i, con 1 <= i <= n, tal que
	Xj = Yj para 1 <= j < i e Xi < Yi.
	  El objetivo del programa es, dados m vectores, cada uno de tamano n,
	implementar un algoritmo que determine el vector minimo utilizando la 
	tecnica Divide y Venceras. Para ello, el programa consta de un procedi-
	miento que recoge el numero de vectores por teclado, asi como las compo-
	nentes de los vectores y los almacena en una matriz. A continuacion, apli-
	cando una tecnica divide y venceras compara los m vectores y devuelve el
	vector minimo. El programa utiliza la tecnica divide y venceras para compa-
	rar los m vectores, asi como para comparar entre las n componentes de los
	vectores. Existen dos alternativas para la comparacion entre las componen-
	tes de dos vectores: la comparacion secuencial y la comparacion D & V. Am-
	bas estan implementadas. 
	 
	Funcionamiento: Debido a que el Pascal - limita bastante nuestra capacidad
	de trabajo, es necesario explicar en este apartado el funcionamiento del
	programa, ya que de lo contrario comprender el resultado que muestra seria
	casi imposible. Al ejecutar el programa este se queda a la espera de que
	el usuario deposite dos valores. El primer valor es el numero de vectores
	a a analizar, que puede ser un valor de 1 - 20. Una vez introducido este
	valor se pulsa Enter, y el programa pide el segundo valor, que es el nu-
	mero de componentes de cada vector (1 - 10). Una vez introducidos ambos
	valores deberemos introducir los vectores por teclado. Cuando acabemos de
	introducir un vector, se mostrara por pantalla un cero, que servira de
	indicio para saber que el siguiente valor que introduzcamos correspondera
	a otro nuevo vector. Una vez introducidos los vectores el programa muestra
	por pantalla los vectores. Cada elemento del vector esta separado por un 0 
	del elemento siguiente, y cada vector se separa de otro tambien por un 0,
	de modo que entre el ultimo elemento de un vector y el primero del siguiente
	existen 2 ceros. Esta es la forma de determinar que elementos corresponden
	a cada vector. A continuacion el programa muestra el vector minimo por dos
	veces, separado de tres ceros. Si el programa funciona correctamente debera
	devolver el mismo valor, y se devuelve dos veces debido a que en la primera
	vez se utiliza la comparacion secuencial entre los elementos de un vector,
	y la segunda utiliza la comparacion D & V. La comparacion entre todos los
	vectores utiliza en ambos casos la tecnica Divide y Venceras.
	
 *************************************************************************}
 


 program practica1;

 const MAXVECTOR = 10;   { Numero maximo de componentes de cada vector }
       MAXMATRIZ = 20;	 { Numero maximo de vectores }
       CERO = 0;
       UNO = 1;

 type vector = array [1..MAXVECTOR] of integer; { Vectores }
      matriz = array [1..MAXMATRIZ] of vector;  { Tipo Matriz de vect }


 var matr: matriz;
     m, n, min: integer;  { M -> Numero de vectores  N -> Numero de compon. }
	  elec: integer;       { elec -> Variable auxiliar }


 {***********************************************************************
  
  MOSTRAR_MATRIZ: Rutina que muestra en pantalla la matriz que contiene los
  m vectores. Debido a las limitaciones de muestreo que ofrece el Pascal -,
  esta rutina muestra todos los vectores separando cada uno de los elementos
  por un cero, asi como separando tambien cada vector de otro por un cero.
  
 ************************************************************************}


 procedure mostrar_matriz (m , n: integer);
 var i, j: integer;

 begin
  i := 1;
  while (i <= m) do begin
   j := 1;
   while (j <= n) do begin
    write (matr[i][j]);
    write (CERO);
    j := j + 1;
   end;
   write (CERO);
   i := i + 1;
  end;
 end;


 {************************************************************************
  
  GENERAR: Genera los m vectores por teclado. Esta rutina espera a que el 
  usuario introduzca por teclado el numero de vectores a crear, asi como el
  numero de elementos de cada vector y luego permanece a la espera de que
  el usuario introduzca los valores y los almacena en una matriz.

  ***********************************************************************}


 procedure generar (var m, n: integer);
 var v: vector;
     i, j: integer;

 begin
  read (m);   { Numero de vectores a crear }
  read (n);   { Numero de componentes de cada vector}
  i := 1;
  while (i <= m) do begin
   j := 1;
   while (j <= n) do begin
    read (matr[i][j]);
    j := j + 1;
   end;
  	write (CERO); 
	i := i + 1;
  end;
  mostrar_matriz (m, n);
 end;

 {************************************************************************
 
  MINIMO: Esta funcion compara secuencialmente las componentes entre dos
 vectores y devuelve	el vector minimo entre ambos. Para ello recorre los vec-
 tores secuencialmente comparando elemento a elemento mientras estos sean
 iguales, y cuando encuentra uno distinto determina el vector minimo y lo
 almacena en la variable min
 
 *************************************************************************}


 procedure minimo (v1, v2, n: integer; var min: integer);
 var i, abort: integer;

 begin
  abort := 0;
  i := 1;
  min := -1;
  while (i <= n) and (abort = 0) do begin
    if (matr[v1][i] <> matr[v2][i]) then begin
      if (matr[v1][i] < matr[v2][i]) then
     	 min := v1
      else
     	 min := v2;
      abort := 1;
    end;
    i := i + 1;
  end;
  if (min = -1) then
  	min := v1;
 end;

 {*************************************************************************
  COMP: Procedimiento que compara dos vectores para determinar cual de ellos
  es minimo utilizando la tecnica Divide y Venceras. Para ello, divide recur-
  sivamente los accesos a los elementos y compara, y cuando encuentra dos
  elementos distintos sale de las llamadas recursivas y devuelve el indice de
  uno de los dos vectores. 
 **************************************************************************}


 procedure comp (v1, v2, izq, der: integer; var min: integer; var abort: integer);
 var medio: integer;

 begin
  if (abort = 0) then begin
    if (izq = der) then begin
      if (matr[v1][izq] <> matr[v2][izq]) then begin
        if (matr[v1][izq] > matr[v2][izq]) then
          min := v2
        else
          min := v1;
        abort := 1;
      end;
    end
    else begin
      medio := (izq + der) div 2;
      comp (v1, v2, izq, medio, min, abort);
      comp (v1, v2, medio + 1, der, min, abort);
    end;
  end;
 end;

 
 {*************************************************************************
 BUSCARMIN: Esta es la rutina que se encarga de realizar la mayor parte del
 proceso. Es el procedimiento que lleva a cabo la determinacion del vector 
 minimo. Se divide recursivamente la matriz y se trabaja en cada iteracion 
 con la mitad de la misma. De este modo se van determinando los vectores 
 minimos de cada "mitad" de la matriz en cada llamada recursiva y al final
 se comparan el minimo de una mitad con el minimo de la otra, siendo el mi-
 nimo de ambos el vector minimo de la matriz. El parametro elec determina el
 tipo de comparacion a realizar. Si se pasa un 0, se compara secuencialmente
 los vectores, y si se pasa un 1, los vectores entre ellos tambien son compa-
 rados mediante la tecnica D & V. (procedimiento comp).  
 *************************************************************************} 

 procedure buscarmin (top, bottom, n, elec: integer; var min: integer);
 var min1, min2, medio, abort: integer;

 begin
  if (top = bottom) then
    min := top
  else
  if (top = bottom - 1) then begin
    if (elec = 0) then
      minimo (top, bottom, n, min)
    else begin
      abort := 0;
      comp (top, bottom, 1, n, min, abort);
      if (abort = 0) then
         min := top;
    end;
  end
  else begin
   medio := (top + bottom) div 2;
   buscarmin (top, medio, n, elec, min1);
   buscarmin (medio + 1, bottom, n, elec, min2);
   if (elec = 0) then
      minimo (min1, min2, n, min)
   else begin
      abort := 0;
      comp (min1, min2, 1, n, min, abort);
      if (abort = 0) then
         min := min1;
   end;
  end;
 end;

 
 {********************************************** Cuerpo del programa *******}


 begin
  generar (m, n);
  elec := CERO;
  while (elec <= 1) do begin
   buscarmin (UNO, m, n, elec, min);
   write (CERO);
   write (CERO);
   write (CERO);
   write (min);
   elec := elec + 1;
  end; 
 end.
