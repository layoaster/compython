{ Practica 1 - Introduccion a los compiladores I
  Ana Lidia Martin Suarez       19/Octubre/2000
  FINALIDAD: Pide por teclado numeros para introducirlos en una cola, hasta
  que esta se llene. Cuando la cola se encuentra completa, comienza a sacar
  los numeros y los imprime por pantalla, hasta que se vacia. Los numeros
  aparecen separados por el SEPARADOR -1.
  El tamano de la cola es la constante MAX_ELEM                           }

program colas;

const MAX_ELEM = 5;              { Tamano de la cola }
      SEPARADOR = 1;


type tcola= array [1..MAX_ELEM] of integer;     { Array cola de MAX_ELEM }

var numero:integer;               { Numero a pedir por teclado }
    llena, vacia: boolean;
    pri, ult: integer;            { Posicion del primer y ultimo elemento }
    cola: tcola;

{ ini_cola: Inicializa la cola. Pone a nulos pri y ult                    }
procedure ini_cola (var cola:tcola);
begin
  pri:= 0;
  ult:= 0;
end;

{ cola_llena: Comprueba si la cola esta llena. La condicion para que se
  encuentre completa es que el ultimo elemento se encuentre una posicion
  por debajo que el primer elemento.
  Devuelve en la variable llena si se encuentra o no completa.         }
procedure cola_llena (cola:tcola; var llena:boolean);
begin
  llena:=false;
  if ult <> MAX_ELEM then     { Si ult NO ocupa la ultima posicion del array }      
  begin
    if ult + 1 = pri then     { Si esta llena }
      llena:= true;
  end
  else                        { Si ult ocupa la ultima posicion del array }
    if pri = 1 then           { Se compara con la primera posicion } 
      llena:= true;
end;

{ cola_vacia: Comprueba si la cola se encuentra vacia. La condicion es
  que pri y ult se encuentren a 0
  Devuelve en la variable vacia el estado de la cola                   }
procedure cola_vacia (cola:tcola; var vacia:boolean);
begin
  vacia:=false;
  if ult = 0 then
    vacia:= true;
end;

{ insertar_cola: Inserta un numero k en la cola. Primero comprueba que no
  se encuentre llena, ni vacia. Si se encuentra vacia, hace apuntar pri al
  primer elemento. Si ult apunta al ultimo elemento del array, entonces 
  pasara a apuntar al primer elemento.                                    }
procedure insertar_cola (k:integer; var cola:tcola);
var llena:boolean;
begin
  cola_llena (cola, llena);
  if llena = false then             { Si la cola NO esta llena }
  begin
    cola_vacia (cola, vacia);
    if vacia=true then              { Si la cola esta vacia }
      pri:= 1;                      { Apunta pri al primer elemento }
    if ult = MAX_ELEM then          { Si ult apunta al ultimo elem. array }
    begin
      ult:= 1;                      { Pasara a apuntar al primer elemento }
    end
    else                            { Si no apunta al ultimo }
      ult:= ult + 1;                { Lo hacemos apuntar al siguiente elem }
    cola [ult]:= k;                 { Introducimos el numero }
  end;
end;

{ sacar_elem: Saca un elemento de la cola. Si pri es igual a ult entonces
  la cola esta vacia y ponemos a nulos pri y ult. Si pri apunta al ultimo
  elemento del array, lo hacemos apuntar al primer elemento. Si no apuntara
  al siguiente elemento.
  k devuelve el numero que sacamos de la cola.                           }
procedure sacar_elem (var k:integer; var cola: tcola);
begin
  k:= cola [pri];
  if pri = ult then                   { Si la cola esta vacia }
    ini_cola (cola)                   { Ponemos a nulos pri y ult }
  else
  begin
    if pri = MAX_ELEM then            { Si pri apunta al ultimo elemento }
    begin
      pri:= 1;                        { Apuntara al primero }
    end
    else                              { Si no apunta al ultimo }
      pri:= pri + 1;                  { Apuntara al siguiente elemento }
  end;
end;

begin
  ini_cola (cola);                    { Inicializo la cola }
  cola_llena (cola, llena);
  while llena = false do              { Mientral la cola no se llene }
  begin
    read (numero);                    { Inserto numeros en la cola }
    insertar_cola (numero, cola);
    cola_llena (cola, llena);
  end;                                { Cuando la cola se llene }
  vacia:= false;
  while vacia = false do              { Y mientras no se vacie }
  begin
    sacar_elem (numero, cola);        { Saco los numeros de la cola }
    write (numero);                   { Y los imprimo por pantalla }
    write (-1*SEPARADOR);
    cola_vacia (cola, vacia);
  end;
end.
