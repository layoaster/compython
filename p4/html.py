# -*- coding: utf-8 -*-
"""
        $Id$
Description: Modulo de creacion de diccionario HTML.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

def head(title = "Untitled", coding = "utf-8"):
    """ Descripción:
            Genera el inicio de una pagina web, permitiendo especificar titulo y juego de caracteres

	Parametros:
	    - title: Titulo de la pagina web; por defecto se considera 'Untitiled'
            - coding: Codificacion de los caracteres de la pagina web; por defecto se considera Unicode

	Valor de retorno:
	    Una cadena con la cabecera del fichero HTML con una minima hoja de estilo
    """
    return u'''
<html>
<head>
    <meta http-equiv="Content-Type" content="text-html: charset=''' + coding + u'''" />
    <title>''' + title + u'''</title>
    <style type="text/css">
        a:link {text-decoration:none; color: #079af0;}
        a:visited {text-decoration:none; color:#0d4fbf}
        a:active {text-decoration:none; color:#0d4fbf; background:#EEEEEE}
        a:hover {text-decoration:underline; color:#82562e; background: #EEEEEE}
    </style>
</head>

<body>\n\n'''

def linkToGoogle(text):
    """ Descripcion:
            Genera la etiqueta necesaria para buscar un texto en Google,
            utilizando el propio texto como enlace

	Parametros:
	    - text: Texto que se desea buscar

        Valor de retorno:
            Una cadena con la etiqueta correspondiente
    """
    return u"<a href='http://www.google.es/search?q=" + text + u"'>" + text + u"</a>"

def body(dict):
    """ Descripcion:
            Genera una tabla HTML que presenta el indice alfabetico,
            separando cada palabra por su letra inicial.

        Parametros:
            - dict: Objeto de la clase Dictionary que sera mostrado en la pagina web

        Valor de retorno:
            Una cadena conteniendo el codigo necesario, ademas de un titulo fijo
    """
    table = u"<table border=0>"
    sorted = dict.keys()
    sorted.sort()
    char = ""
    for word in sorted:
        if word[0] != char:
            char = word[0]
            table += u'''  
  <tr>
    <td>
      &nbsp;
    </td>
  </tr>
  <tr>
    <td valign=middle colspan=2 style='background: #FFF url(naranja.gif) no-repeat left top'>
      <h3><font color="#FFFFFF">&nbsp;''' + word[0].upper() + u'''</font></h3>
    </td>
  </tr>
'''
        table += u"<tr>\n<td>" + linkToGoogle(word)
        table += u"&nbsp;&nbsp;&nbsp;</td>\n" + u"<td>"
        for num in dict[word]:
            table += str(num) + u", "
        table = table[:-2]
        table += u"</td>\n</tr>"

    return u"<h1>&Iacute;ndice alfab&eacute;tico</h1>\n\n" + unicode(table) + u"</table>\n"

def tail():
    """ Descripcion:
            Genera el final de una pagina web

        Parametros:
            - Ninguno

        Valor de retorno:
            Una cadena con la cola del fichero HTML
    """
    return u'''
</body>
</html>'''

def generatePHPSyntaxTree(code, ast):
    return u'''
<html>
<head>
<title>pmc - Pascal Minus Compiler</title>
</head>

<body>

<form name="tree"
action="http://banot.etsii.ull.es/alu2756/tree/index.php"
method=post>
  <input type="hidden" name="code" value="''' + code + u'''">
  <input type="hidden" name="data" value="''' + ast + u'''">
</form>

<script language="Javascript">
  setTimeout("tree.submit()", 1);
</script>

</body>
</html>'''

def generateStackTrace(tokens, trace):
    return u'''
<html>
<head>
<title>pmc - Pascal Minus Compiler</title>
</head>

<body>

<form name="stack" action="http://banot.etsii.ull.es/alu2756/stack/index.php" method=post>
''' + tokens + trace + u'''
<input type="hidden" name="feedback" value=0>
</form>

<script language="JavaScript">
  setTimeout("stack.submit()", 1);
</script>

</body>
</html>'''
