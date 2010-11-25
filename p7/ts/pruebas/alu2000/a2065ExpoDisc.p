{////////////////////////////////////////////////////////////////////////////
// Practicas (COMPILADORES) 3 De Informatica.                              //
// Autor:         Jose Victor Garcia Roman.                                //
// Fecha:         17.10.2000                                               //
// PROGRAMA:      comp_01.p                                                //
// FINALIDAD:     Programa de ejemplo para comprobar las caracteristicas   //
//                del lenguaje de programacion pascal-.                    //
// USO:           Al principio el programa pide la opcion para uno de los  //
//                siguientes apartados (la opcion es un numero entero):    //
//                 si la opcion introducida es el numero 0.                //
//                  - EXPONENCIACION DISCRETA.                             //
//                    Resuelve el problema a^m (mod n) de forma rapida.    //
//                   * Pide "a" por teclado                                //
//                   * Pide "m" por teclado                                //
//                   * Pide "n" por teclado                                //
//                   * Muestra la solucion a^m (mod n) por pantalla        //
//                 si la opcion introducida es el numero 1.                //
//                  - MCD                                                  //
//                    Resuelve el problema mcd(a,b) por el algoritmo de    //
//                    Euclides.                                            //
//                   * Pide "a" por teclado                                //
//                   * Pide "b" por teclado                                //
//                   * Muestra la solucion mcd(a,b) por pantalla           //
//                 si la opcion introducida es el numero 2.                //
//                  - Inverso                                              //
//                    Resuelve el problema a^-1(mod b) por el algoritmo de //
//                    Euclides.                                            //
//                   * Pide "a" por teclado                                //
//                   * Pide "b" por teclado                                //
//                   * Muestra la solucion a^-1(mod b) por pantalla        //
////////////////////////////////////////////////////////////////////////////}
program exponDiscreta_MCD_Inverso;

var a:integer;
	 b:integer;
	 m:integer;
	 n:integer;
	 devolver:integer;

{////////////////////////////////////////////////////////////////////////////
// Procedimiento que calcula el maximo entre dos n£mero enteros y los      //
// retorna en el parametro devuelve.                                       //
////////////////////////////////////////////////////////////////////////////}
procedure MAX (var devuelve:integer;a:integer; b:integer);
begin
  if (a > b) then devuelve := a
  else devuelve := b;
end;

{////////////////////////////////////////////////////////////////////////////
// Procedimiento que resuelve el problema de exponenciacion discreta con   //
// el algoritmo rapido a^m (mod n).                                        //
// Parametros: devuelve, es un integer donde es devuelto el resultado.     //
//             a, m, n : integer que corresponden a los datos de entrada.  //
////////////////////////////////////////////////////////////////////////////}
procedure ExponDiscreta (var devuelve:integer; a:integer; m:integer; n:integer);
var x : integer;
    atemp : integer;  { variables temporales que almacenan el estado }
    mtemp : integer;  { del algoritmo }

begin
  x := 1;
  atemp := a;
  mtemp := m;

  while (mtemp > 0) do
  begin
    while ((mtemp mod 2) = 0) do
    begin
      mtemp := mtemp div 2;
      atemp := (atemp * atemp) mod n;
    end;
    mtemp := mtemp - 1;
    x := (x * atemp) mod n;
  end;
  devuelve := x;
end;

{////////////////////////////////////////////////////////////////////////////
// Procedimiento que implementa el algoritmo de Euclides para calcular el  //
// maximo comun divisor entre dos numeros.                                 //
// Parametros : devuelve, es un integer donde retorna el resultado del mcd //
//              a, b: son los integer donde se pasan los datos de entrada  //
////////////////////////////////////////////////////////////////////////////}
procedure mcd (var devuelve:integer; a:integer; b:integer);
var g0:integer;   { variables que simulan el vector de terminos }
    g1:integer;   { del algoritmo de euclides }
    temp:integer;

begin

  if (a > b) then   { Siempre se almacena en g0 el MIN(a,b) }
  begin
    g0 := a;
    g1 := b;
  end
  else
  begin
    g0 := b;
    g1 := a;
  end;

  while (g1 > 0) do
  begin
    temp := g1;              { Algoritmo de Euclides}
    g1 := g0 mod g1;         { Gi+1 = Gi-1 mod Gi   }
    g0 := temp;              
  end;
  devuelve := g0;
end;
{////////////////////////////////////////////////////////////////////////////
// Procedimiento que implementa el algoritmo de Euclides para calcular el  //
// inverso de un numero utilizando aritmetica modular, se basa en el       //
// algoritmo maximo comun divisor entre dos numeros.                       //
// Parametros : devuelve, es un integer donde retorna el resultado del     //
//              Inverso a^-1 (mod b).                                      //
//              a, b: son los integer donde se pasan los datos de entrada  //
////////////////////////////////////////////////////////////////////////////}
procedure Inverso (var devuelve:integer; a:integer; b:integer);
var g0, g1 :integer;    { variables que simulan el vector de terminos }
    c, x0, x1 :integer;
    temp :integer;

begin
  x0 := 0;
  x1 := 1;

  if (a > b) then   { Siempre se almacena en g0 el MIN(a,b) }
  begin
    g0 := a;
    g1 := b;
  end
  else
  begin
    g0 := b;
    g1 := a;
  end;

  while (g1 <> 1) do
  begin
    c := g0 div g1;               { Ci = Gi-1 / Gi         }

    temp := g1;                   { Algoritmo de Euclides  }
    g1 := g0 mod g1;              { Gi+1 = Gi-1 mod Gi     }
    g0 := temp;              

    temp := x1;
    x1 := -1 * c * x1 + x0;       { Xi = -Ci * Xi-1 + Xi-2 }
    x0 := temp;
  end;
  MAX(temp, a, b);
  if (x1 < 0) then        { si el resultado del inverso es negativo, }
    x1 := x1 + temp;      { pasarlo a la forma positiva (mod b) }
  devuelve := x1;
end;

BEGIN
  read(devolver);   { Se pide por teclado la opcion que se desee}
  if (devolver = 0) then
  begin
    read(a);
    read(m);
    read(n);
    ExponDiscreta(devolver, a, m, n);
    write(devolver);
  end
  else if (devolver = 1) then
  begin
    read(a);
    read(m);
    MCD(devolver, a, m);
    write(devolver);
  end else if (devolver = 2) then
  begin
    read(a);
    read(m);
    Inverso (devolver, a, m);
    write(devolver);
  end;
END.
