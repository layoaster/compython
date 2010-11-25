{***************************************************************************
PRµCTICA:       1
OBJETIVO:       Implementaci¢n del m‚todo de ordenaci¢n HeapSort en Pascal-
FECHA:          18/10/2000
AUTOR:          Iv n Siliuto Beltr n
BIBLIOGRAFÖA:   Apuntes de Metodolog¡a de la Programaci¢n II
ENTRADA:        Introducir 10 numeros enteros para su ordenacion
***************************************************************************}
program Ordenacion_HeapSort;

const
    NUMELE = 10;
    { N£mero de elementos a ordenar }

type
    TipoArray = array[1..NUMELE] of integer;
    { Tipo array para guardar la lista de n£meros }

var
    Lista: TipoArray;   { Array donde se guardan los n£meros }
    i:     integer;     { Öndice para recorrer la lista e introducir datos }


{***************************************************************************
Procedimiento que realiza la ordenaci¢n del array Lista con el m‚todo
HeapSort.
***************************************************************************}
procedure HeapSort;
    var
        First,          { Öndice del primer elemento a ordenar }
        Last,           { Öndice del £ltimo elemento a ordenar }
        Clave: integer; { Variable temporal para realizar intercambios }

    { Realiza un mont¡culo de los n£meros almacenados en Lista }
    procedure HacerMonticulo(First, Last: integer);
        var
            i, j, Clave:   integer;
            Cambio:        boolean;

        begin
            i := First;
            j := 2 * i;
            Clave := Lista[i];
            Cambio := true;
            while (j < Last) and (Cambio) do
            begin
                Cambio := false;
                if i < Last then
                    if Lista[j + 1] < Lista[j] then
                        j := j + 1;
                if Lista[j] < Lista[i] then
                begin
                    Lista[i] := Lista[j];
                    Lista[j] := Clave;
                    i := j;
                    j := 2 * i;
                    Cambio := true;
                end;
            end;
        end;
begin
    First := (NUMELE div 2) + 1;
    Last := NUMELE;
    while First > 1 do
    begin
        First := First - 1;
        HacerMonticulo(First, Last);
    end;
    while Last > 1 do
    begin
        Clave := Lista[1];
        Lista[1] := Lista[Last];
        Lista[Last] := Clave;
        Last := Last - 1;
        HacerMonticulo(First, Last);
    end;
end;

{***************************************************************************
***************************************************************************}
begin
    { Introducimos los elementos en la lista }
    i := 1;
    while (i <= NUMELE) do
    begin
        read(Lista[i]);
        i := i + 1
    end;
    { Realizamos la ordenaci¢n }
    HeapSort;
    { Mostramos la lista ya ordenada }
    i := 1;
    while i <= NUMELE do
    begin
        write((-1) * Lista[i]);
        i := i + 1
    end;
end.
