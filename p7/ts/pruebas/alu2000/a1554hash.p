{*************************************************************************
  TITULO DE LA PRACTICA : Implementacion de un sencillo programa en Pascal
   menos, (HASHING).
  ASIGNATURA : Compiladores 1.
  AUTOR : Jose Fabian leon Campos
  COMENTARIO : Una tecnica para almacenar datos en una array, de modo que
               pueda ser recuperado de un modo eficiente, se denomina con_
               version de claves(hashing). Esta consiste en convertir una
               clave en un indice de table de indices o de busqueda valida
               donde se almacenan los diferentes registros del array. Se
               necesita una funcion de conversion o funcion hash; que con_
               vierta la clave en el ¡ndice del array de elementos; utili_
               zaremos en nuestro caso la funcion modulo.
                  El fenomeno de las colisiones lo evitaremnos mediante
               direccionamiento cerrado:
                  - Inicializar el array.
                  - Calcular la funcion de conversion para la clave.
                  - Situar la nueva clave en la tabla sin posicion libre,
                  si no ir a la siguiente posicion y repetir el proceso.

  FUNCIONAMIENTO : Se debera introducir enteros uno a uno, automaticamente
               el programa nos indicara el resultado de su insercion en la
               tabla hash mediante:
                  1 -> se ha introducido de forma correcta el n£mero.
                  2 -> se encuentra llena la tabla.
                  valor = al introducido  -> ya existe en la tabla.
               Este proceso se repetira hasta que introduzcamos un 0 o la
               tabla este llena.
               Al final se sacara por pantalla toda la tabla.
***************************************************************************}
program hashing;
const
   SIZE_TABLE = 5;   { tamano de la tabla hash}
   input = 1;        { se ha introducido de forma correcta el num en tabla}
   lleno = 22222;    { la tabla esta llena}
   exit = 0;
type
   vector = array[1..SIZE_TABLE] of integer;

{fijar el valor de cada elemento del array igual a -1, para indicar que
ninguna posicion este ocupada
INPUT : A es el array donde almacenamos los numeros, se devolvera por variable
OUTPUT : A inicializado todo a -1.}

procedure inicializar (var  A: vector);
var
   i : integer;
begin
   i := 1;
   while (i <= SIZE_TABLE) do
      begin
         A[i] := -1;
         i := i+1;
      end;
end;

{ FUNCION HASH 
INPUT : num que corresponde al valor introducido por teclado
OUTPUT : num -> posicion que le corresponde en el array}

procedure Hash (var num : integer);
var aux : integer;
begin
   aux := num;
   num := (aux mod SIZE_TABLE) + 1;
end;

{ PROCEDURE INSERTAR la clave en la tabla
INPUT : A es el array donde almacenamos los numeros, se devolvera por variable
        valor -> dato introducido por teclado
        full -> variable indicadora de que esta llena la tabla de numros
OUTPUT : A posiblemente con nuevos numeros
         full indicando si se ha llenado la tabla de nuemros}

procedure insertar (var A : vector; valor : integer; var full: integer);
var pos, cuenta: integer;
begin
   pos := valor;
   Hash(pos); {averiguamos la posicion en la tabla del numero introducido}
   cuenta := 1; {indicadora que hemos recorrido toda la tabla}
   { para seguir avanzando se deben cumplir las 3 condiciones simult.}
   while (A[pos] <> -1) and (A[pos] <> valor) and (cuenta < SIZE_TABLE) do
      begin
         Hash(pos);
         {pos := (pos mod SIZE_TABLE) +1;}
         cuenta := cuenta +1;
      end;
  if (A[pos] = valor) then  {si ya existe tal valor en la tbla no se mete}
      begin
         write(valor);
         write(0);
      end
  else
      if (A[pos] = -1) then   {si no esta y hay hueco libre lo metemos}
         begin
            A[pos] := valor;
            write(input);
            write(0);
         end
      else
         begin
            write(lleno);    { si no, no se mete porque la tabla esta llena}
            write(0);
            full := 1;
         end;
end;

{ PROCEDURE RECORRER la tabla para sacar por pantalla
INPUT : A tabla de numeros}

procedure recorrer( A: vector);
var i : integer;
begin
   i := 1;
   while i<= SIZE_TABLE do
      begin
         write(A[i]);
         write(0);
         i := i+1;
      end;
end;

{ PROCEDURE MAIN que lleva a cabo los procesos de inicializacion del array
   lectura de los numeros, insertarlos en la tabla y su recorrido}
procedure main;
var tabla : vector;
   dato, llena : integer;
begin
   llena := 0; { la tabla se encuentra vacia}
   inicializar(tabla);
   read(dato);
   while (dato <> exit) and (llena <> 1) do { mientras se quiera meter datos}
      begin                              { y la tabla no se llene adelante}
         insertar(tabla, dato, llena);
         if (llena <> 1) then read(dato);
      end;
   if llena <> 1 then write(lleno);
   recorrer(tabla);
end;
   
{ PROGRAMA PRINCIPAL }
begin
   main;
end.
