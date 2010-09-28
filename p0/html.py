# -*- coding: utf-8 -*-
"""
        $Id$
Description: Modulo de creacion de diccionario HTML.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

def head(title = "Untitled"):
    """Cabeceras de html"""
    return '''
<html>
<head>
    <title>''' + title + '''</title>
    <style type="text/css">
        a:link {text-decoration:none; color: #99CC00;}
        a:visited {text-decoration:none; color:#99CC66}
        a:active {text-decoration:none; color:#99FF00; background:#EEEEEE}
        a:hover {text-decoration:underline; color:#99FF00; background: #EEEEEE}
    </style>
</head>

<body>\n\n'''

def linkToGoogle(text):
    """Enlaza el texto a Google"""
    return "<a href='http://www.google.es/search?q=" + text + "'>" + text + "</a>"

def body(dict):
    table = "<table border=0>\n"
    sorted = dict.keys()
    sorted.sort()
    for word in sorted:
        table = table + "<tr>\n<td>" + linkToGoogle(str(word))
        table = table + "&nbsp;&nbsp;&nbsp;</td>\n" + "<td>"
        for num in dict[word]:
            table = table + str(num) + ", "
        table = table[:-2]
        table = table + "</td>\n</tr>\n"
    return table + "</table>\n"

def tail():
    """Final de html"""
    return '''
</body>
</html>'''
