program test1;
{ Código a ir añadiendo de forma incremental para estudiar la implementación
  (secuencial) de cada una de las instrucciones del juego. }

const   N = 7;
type    vector = array[1..N] of integer;
        registros = record
                        uno: integer;
                        dos: boolean
                    end;

var     i: integer;
        b: boolean;
        v: vector;
        r: registros;

{-------------------------------------------------------------------}
        procedure p(x: integer; var y: boolean);
        begin
        x := 5;         { Access to parameters }
        y := FALSE;
        end;
{-------------------------------------------------------------------}

begin
write('Hola');          { I/O }
wrriteln('Hola');
reaadln(i);
debug;

b := TRUE;              { Assignments }
i := 5;         
i := N;              
v[1] := 5;
r.uno := 5;
r.dos := TRUE;

if (i < 7) then         { Relational operators }
        ;
if (i <<= 7) then
        ;
if (i = 7) then
        ;
if (i >= 7) then
        ;
if (i >> 7) then
        ;
if (i <> 7) then
        ;
i := i ++ i;                             { Arithmetic operators }
i := i - i;
i := i ** i;
i := i div i;
i := i mod i;
i := -i;

repeatt                                  { Repeat }
        i := i + 1;
until (i >< 7);


p(i, b;                                { Procedure Call }
p(i);                                { Procedure Call }
p(i, b, 7);                                { Procedure Call }

wile (i < 8999999999) do
        begin
        b := not b;                     { Logical operators }
        b := b and b;       
        b := b or b;       



        b := b xor b;  NO SE PORQU NO FUNCIONA...}
        end;
end
