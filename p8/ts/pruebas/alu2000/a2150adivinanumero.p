{****************************************************************************
 PRÁCTICA NUMERO 1. Elaboración de un programa en pascal-.
 PROFESOR DE LA ASIGNATURA: Francisco de Sande.
 DECHA DE ENTREGA: 19-10-2000.
 ASIGNATURA: COMPILADORES I.
 OBJETIVO: El objetivo de la práctica es el de familiarizarse con el lenguaje
 pascal-, para el posterior desarrollo de un compilador para este lenguaje.
 DESCRIPCIÓN DEL PROGRAMA: La práctica consiste basicamente en adivinar
 comprendidos en un rango determinado de valores. La estructura del programa
 consta de un vector global que almacena un conjunto de diez numeros,
 predefinidos. El usuario tendrá que intentar adivinar alguno de esos diez
 numeros introduciendolos por teclado. Por pantalla se comunicará si el
 numero introducido está en la lista (2), si ya introdujo ese numero (3), o
 si el numero no es correcto. Ejemplo
                     - 123  Introducimos el 23
                     - 413  el numero no se encuentra, e introducimos el 3
                     - 21   lo encuentra y ...
                     - ...
 El (1) significa que espera un numero. El cero es para salir
****************************************************************************}

Program Prueba;
const
    LIMITE = 10;
{Constante que define el limite del vector de numeros que empleamos}
type
    celdas = record        {Esta es la estructura de los registros de numeros}
    	valor: integer;                               {El valor que contienen}
        existe: boolean                           { Si ya se eligio el numero}
        end;
    vector = array [1..10] of celdas;                      {Vector de numeros}

Var
    numero, i: integer;                                      {Numero a buscar}
    registro: vector;                                      {Vector de numeros}
    existe, existia: boolean;         {El numero puede existir o ser repetido}

{Esta funcion se encarga de inicializar el vector de numeros en donde}
{realizaremos las busquedas}
Procedure inicializar (var reg: vector);
    var
	    i: integer;                                        {Variable contador}

    begin
    	i := 1;
    	while (i <= LIMITE) do
            begin
	            reg[i].valor := (i*6) div 2;     {Inicializacion de los campos}
  	            reg[i].existe := FALSE;
	            i := i + 1;
  	        end;
    end;

{Esta funcion se encarga de buscar en el vector de numeros si el que nosotros}
{hemos introducido existia o existe, y el procedimiento nos lo devuelve por}
{los parametros pasados por variable ex1, ex2.}
Procedure buscar_numero (reg: vector; num: integer; var ex1: boolean;
                         var ex2: boolean);
    var
	    i: integer;                                        {Variable contador}

    begin
        i := 1;
        ex1 := FALSE;
        ex2 := FALSE;
        while (i <= LIMITE) do
            begin
                if ((reg[i].valor = num) and          {El numero existia}
                                         (reg[i].existe = TRUE)) then
                    ex2 := TRUE;
                if ((reg[i].valor = num) and
                                         (reg[i].existe = FALSE)) then
                    begin
                        ex1 := TRUE;                        {El numero existe}
                        reg[i].existe := TRUE;
                    end;
                i := i + 1;
            end;
    end;

Begin
	inicializar (registro);
    numero := 1;
    while (numero <> 0) do
        begin
            write (1);                  {El 1 indica que escribamos un numero}
            read (numero);
            buscar_numero (registro, numero, existe, existia);
            if (existe = TRUE) then
                write (2);                  {El 2 indica que el numero existe}
            if (existia = TRUE) then
                write (3);                 {El 3 indica que el numero existia}
            if ((existia = FALSE) and (existe = FALSE)) then
                write (4);               {El 4 indica que el numero no existe}
        end;
End.
