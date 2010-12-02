{*****************************************************************************
PROGRAMA: Problema de la mochila (Compiladores I - 01)
AUTOR: Ubay Dorta Guerra
FECHA: 19.10.2000
FINALIDAD:	Implementar un programa que resuelva el problema de la mochila.
            El problema de la mochila consiste, en que dada una mochila
            con una capacidad y una serie de objetos con unos pesos y valores,
            maximizemos el valor de la mochila metiendo en ella objetos,
            teniendo en cuenta que la suma de sus pesos, no sea mayor que la
            capacidad de la mochila.
COMENTARIOS: Para resolver este problema se utiliza un algoritmo de
             programacion dinamica que encuentra la solucion optima.
MODO DE USO: Introducir en primer lugar el numero de objetos, luego la
             capacidad de la mochila, luego para cada objeto introducir peso
             y valor. El programa dara como resultado: el valor optimo de la
             mochila y la composicion de esta, mostrando numero de objeto,
             peso del objeto y valor.
PROBLEMA EN COMPILADOR DE UNIX: No puedo usar vector de un tipo record porque
				 me cambia valores de otras variables. Este problema se puede
				 ver en el procedimiento obten_datos ya que al principio se
				 pide el n_obj (numero de objetos) y despues al escribir en     
				 el array del tipo record se me cambia el valor de n_obj. 
				 En el procedimiento se han incluido 2 write que lo muestran.
*****************************************************************************}
program problema_mochila;

const MAX_ELEM = 15;   {Numero maximo de elementos de los arrays}

type vect_int = array[0..MAX_ELEM] of integer;   {Tipo vector de enteros}
     matriz = array[1..MAX_ELEM] of vect_int;    {Tipo matriz de enteros}
     prop_obj = record   {Propiedades del objeto}
              peso, valor:integer    {Peso y valor del objeto}
              end;
     vect_obj = array [1..MAX_ELEM] of prop_obj;  {Tipo vector de objetos}

{****************************VARIABLES GLOBALES******************************}
var n_obj:integer;       {Numero de objetos disponibles}
    peso_moch:integer;   {Peso maximo que aguanta la mochila, capacidad}
    tabla:matriz;        {Tabla para algoritmo de programacion dinamica}
    objeto:vect_obj;     {Vector de objetos disponibles}
{*****************************************************************************
* inic_arrays -- Inicializa los vectores uni y bidimensionales a 0.
*****************************************************************************}
procedure inic_arrays;
var i,
    j:integer;

begin
   i := 1;
   while (i <= n_obj) do
   begin
      objeto[i].peso := 0;
      objeto[i].valor := 0;
      j := 0;
      while (j <= peso_moch) do
      begin
         tabla[i][j] := 0;
         j := j + 1;
      end;
      i := i + 1;
   end;
end;
{*****************************************************************************
* obten_datos -- Toma por teclado los datos de: numero de objetos, peso maximo
*					  de la mochila, peso y valor de cada objeto.
*****************************************************************************}
procedure obten_datos;
var i:integer;

begin
   read(n_obj);
   read(peso_moch);
{   inic_arrays;}   {Quitamos esto para ver el problema}
   i := 1;
   while (i <= n_obj) do
   begin
		write(n_obj);   {Se muestra el valor correcto de n_obj} 
      read(objeto[i].peso);
		write(n_obj);	 {El valor de n_obj ha cambiado}
      read(objeto[i].valor);
      i := i + 1;
   end;
end;
{*****************************************************************************
* maximo -- Nos dice que valor de la mochila es el optimo para cada
*           subproblema (casilla). Para una casilla i, j elegiremos el maximo
*           entre: coger el valor que habia en i - 1, j, es decir no teniendo
*           en cuenta el objeto de la fila actual i, o sumar el valor del
*           objeto i con el valor de la casilla i - 1, j - 'peso de i', esto
*				es, sumar el valor del objeto nuevo de la fila 'i' con el que ya
*           habia, cuando la capacidad de la mochila era tal
*           que sumado al peso del objeto i no se rebase la capacidad actual
*           j.
*
* Parametros :
*			i -- Numero de fila de la casilla (subproblema).
*        j -- Numero de columna de la casilla (subproblema).
*        val_max -- Valor maximo entre las dos posibildades.
*****************************************************************************}
procedure maximo(i, j:integer;var val_max:integer);
begin
   if ((j - objeto[i].peso) < 0) then  {Si execederemos negativamente matriz}
      val_max := tabla[i - 1][j]   {Cogemos el valor sin objeto 'i'}
   else
   begin  {Se elige entre las dos posibilidades}
      if (objeto[i].valor + tabla[i - 1][j - objeto[i].peso]) >
         (tabla[i - 1][j]) then
         val_max := (objeto[i].valor + tabla[i - 1][j - objeto[i].peso])
      else
         val_max := tabla[i - 1][j];
   end;
end;
{*****************************************************************************
* mochila -- Este procedimiento implementa un algoritmo de programacion
*            dinamica para resolver el problema de la mochila. Este algortimo
*            va generando una tabla en el que el numero de filas es el numero
*            de objetos (cada fila representa a un objeto) y el numero de
*            columnas son todos las posibles capacidades (enteras) entre 0
*            y la capacidad dada de la mochila. En cada casilla de la tabla se
*            va resolviendo un subproblema de modo que el significado de estar
*            en la posicion 'tabla[i][j]' es: valor maximo de la mochila
*            cuando la capacidad de la mochila es 'j' usando solo objetos
*            menores o iguales a 'i'. Por tanto cuando lleguemos a la fila
*            'numero de objetos' y a la columna 'capacidad dada de la mochila'
*            resolveremos en esa casilla el problema de: el valor maximo de
*            la mochila cuando su capacidad es el que le dimos al principio
*            usando todos los objetos posibles. Para calcular el valor en cada
*            casilla se utiliza el procedimiento maximo.
*****************************************************************************}
procedure mochila;
var i,
    j:integer;
    val_max:integer;   {Valor maximo en cada casilla}

begin
   i := 1;
   while (i <= n_obj) do
   begin
      j := 1;
      while (j <= peso_moch) do
      begin
         if (i = 1) then
         begin
            if (objeto[i].peso <= j) then
            {Fila 1 y peso objeto <= que capacidad en columna j -> cogerlo}
               tabla[i][j] := objeto[i].valor
            else
               tabla[i][j] := 0;
         end
         else
         begin
            maximo(i, j, val_max);  {Buscar el valor maximo para subproblema}
            tabla[i][j]:=val_max;
         end;
         j := j + 1;
      end;
      i := i + 1;
   end;
   if ((peso_moch = 0) or (n_obj = 0)) then
      write(0)
   else
      write(tabla[n_obj][peso_moch]);  {Resultado final: valor optimo mochila}
end;
{*****************************************************************************
* composicion -- Nos dice que elementos hay en la mochila para que esta tenga
*                una valor optimo. Para resolver este problema nos
*                posicionamos en la ultima casilla de la tabla formada y vamos
*                a ir subiendo por la misma columna hasta que el valor de la
*                casilla en la fila i sea distinta a la de la fila i - 1,
*                en ese caso sabremos que el objeto 'i' esta en la mochila.
*                Una vez hecho esto la capacidad de la mochila sera la que
*                habia, menos el peso del objeto que sabemos esta en la
*                mochila, por tanto nos movemos a la columna que indique
*                esa capacidad. Repetimos el proceso hasta que lleguemos a
*                una casilla donde el valor sea 0, es decir no se puedan
*                coger mas objetos.
*****************************************************************************}
procedure composicion;
var val_opt,   {Valor optimo de la mochila, ultima casilla de tabla}
    i,
    j:integer;

begin
   i := n_obj;
   j := peso_moch;
   if ((peso_moch = 0) or (n_obj = 0)) then  {Si no posibles objetos en moch}
      val_opt := 0  {No tendra valor la mochila}
   else
      val_opt := tabla[i][j];
   while ((val_opt > 0) and (i - 1 > 0)) do  {Hasta no poder coger mas objs}
   begin
      if (tabla[i][j] = tabla[i - 1][j]) then
         i := i - 1
      else
      begin
         write(i);
         write(objeto[i].peso);
         write(objeto[i].valor);
         j := j - objeto[i].peso;  {Nueva capacidad de mochila}
         val_opt := val_opt - objeto[i].valor;
         i := i - 1;
     end;
   end;
   if ((i - 1 <= 0) and (val_opt > 0)) then  {Si en fila uno y falta objeto}
   begin
      write(i);   {Cogemos el objeto 1}
      write(objeto[i].peso);
      write(objeto[i].valor);
   end;
end;
{*****************************************************************************
* programa ppal. -- Llama a los procedimientos de iniciar arrays, obtener
*                   datos, calcular el valor optimo y composicion de la
*                   mochila.
*****************************************************************************}
begin
    obten_datos;
    mochila;
    composicion;
end.
