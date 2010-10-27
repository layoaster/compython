{
    Alumno: Fernando Arvelo Rosales             alu1661
    Programa: alu1661.p
    Descripci¢n: 
        Programa Dise¤ado para probar el analizador sintactico de pascal -
      con recuperaci¢n de errores en modo panico.
    Notas:
        Este fichero fue realizado con tabuladores de longitud 8. Para
      visualizarlo correctamente hay que usar un editor que tenga esto en
      cuenta.
} 
Program alu1661;  
Const
    jauja = 7;
    mojama = -2;        {Error, constantes negativas no permitidas}
    Abracadabra = 25;
    chungani = 345      {Error, falta punto y coma (se detecta en la    }
    Gonzo = jauja;      {                               siguiente linea)}
    Cucucu = 4;
Type
    Paraiso = Array [cucucu..jauja] of integer;
    mirregistro = Record 
                        f := Paraiso;   { Error, Becomes no valido}
                        i : integer;
                  end;
    mas_regs = Record a,b: integer end;
    Arraymalo = Array [1..<6] of boolean;        { Error, "<" no valido }
    Unarray = Array [1..2] of boolean;
Vir                             { Error, Identificador no esperado.}
  me_la_salto : integer;
  tambien_me_la_salto : Boolean;

Procedure NoHacerNada;
var 
    x : Integer;
    y := Meequivoco            { Error, Becomes no valido }
    jander : Paraiso;
    
Begin
    jander [cucucu + 2] := Abracadabra; 
    jander [+ 3] := Abracadabra;        { Error, expresion incorrecta }
    write (jander [(2+3) mul (5 - 4)]);
    write x);                           { Error, falta abrir parentesis }
    if x > 4 then
    began               { Error: 2 identificadores consecutivos }
        x := 4;
        x := 5;
    end;                { Este "end" casa con el begin del procedimiento, lo
                          cual es incorrecto            }     
End;                    { Error, End no esperado, esperamos un begin }

Begun                                           {error}
    jander [cucucu + 2] := Abracadabra;         {error}
    write (jander [(2+3) mul (5 - 4)]);         {error}
    if 1 > 2 then                               {error}
    begin               { Este begin es considerado el begin del programa }
      :=                {error}
    end;                {error}
.

    
    

