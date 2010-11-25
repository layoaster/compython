{Alumno: Pablo G¢mez Ascanio
Pr ctica: N§1 de compiladores, programa en pascal-
La idea de este programa es dado un n£mero cualquiera,
hallar los n£meros primos que hayan hasta ‚l y luego descomponerlo
en sus factores primos}
{funcionamiento: Pide un numero de entrada y luego muestra en pantalla la descomposicion en factores separados por -1000}
program primos;
const
     UNO = 1;
     DOS = 2;
     CERO = 0;
     TOPE = 1000;
type
    {Defino un tipo matriz}
    numero = array [UNO .. TOPE] of integer;
var
    {valores contendr  un uno si el n£mero es primo otro si no}
    valores: numero;
    i, j, dato:integer; {Contadores de pr¢posito general}

procedure  a_pantalla (valor:integer); {Pone en pantalla los n£meros primos
y la descomposici¢n separados por ceros}
var
   descompone:integer;
           begin
                i := valor;
                descompone := valor;
                while (i > UNO) do
                      begin
                           if (valores[i] = 1) then
                              begin
                                   if ( descompone mod i = 0) then
                                      begin
                                        descompone := descompone div i;
                                        write(i);
					write(-1);
					write(CERO);
					write(CERO);
					write(CERO);
                                      end
                                   else
                                       i := i - UNO;
                              end
                                 else
                                     i := i - UNO;
                      end;
           end;

begin
      i := UNO;
      while (i <= TOPE) do    {Inicializa a uno la matriz}
            begin
                 valores[i] := UNO;
                 i := i + UNO;
            end;
      j := DOS;
      read (dato);
      if (dato <= TOPE) then
        begin
             while (j <= dato) do
                   begin
                        if (valores[j] = UNO) then
                           begin
                                i := j;
                                  while (i <= dato) do
                                        begin
                                          i := i + j;
                                          if (i <= dato) then valores[i] := j;
                                          {va poniendo el n§ por
                                            el que es divisible}
                                        end;
                                  end;
                                j := j + UNO;
                   end;
             a_pantalla(dato);
        end;
end.
