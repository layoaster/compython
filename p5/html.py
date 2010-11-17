# -*- coding: utf-8 -*-
"""
        $Id: html.py 69 2010-09-29 15:58:18Z s.armasperez $
Description: Modulo de creacion de Arbol de Analisis Sintactico en formato HTML.
    $Author: s.armasperez $ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date: 2010-09-29 16:58:18 +0100 (mié 29 de sep de 2010) $
  $Revision: 69 $
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

def generatePHPSyntaxTree(code, ast, sequences, dpt):
    page = '''
<html>
<head>
<title>pmc - Pascal Minus Compiler</title>
</head>

<body>

<form name="tree"
action="http://banot.etsii.ull.es/alu2756/tree/ast/index.php"
method=post>
  <input type="hidden" name="code" value="''' + code + u'''">
  <input type="hidden" name="dpt" value="''' + dpt + u'''">
  <input type="hidden" name="ast" value="''' + ast + u'''">
  <input type="hidden" name="preorder" value="'''
    for i in sequences[0]:
        page += str(i) + u''' '''
    page += u'''">
  <input type="hidden" name="inorder" value="'''
    for i in sequences[1]:
        page += str(i) + u''' '''
    page += u'''">
  <input type="hidden" name="postorder" value="'''
    for i in sequences[2]:
        page += str(i) + u''' '''
    page += u'''">
</form>

<script language="Javascript">
  setTimeout("tree.submit()", 1);
</script>

</body>
</html>'''
    return page
