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
</head>

<body>\n\n'''

def linkToGoogle(text):
    """Enlaza el texto a Google"""
    return "<a href='http://www.google.es/search?q=" + text + "'>" + text + "</a>"

def writeDictionary(d):
    table = "<table border=0>\n"
    sorted = d.keys()
    sorted.sort()
    for word in sorted:
        table = table + "<tr>\n<td>" + linkToGoogle(str(word))
        table = table + "&nbsp;&nbsp;&nbsp;</td>\n" + "<td>"
        for num in d[word]:
            table = table + str(num) + ", "
        table = table[:-2]
        table = table + "</td>\n</tr>\n"
    return table + "</table>\n"

def end():
    """Final de html"""
    return '''
</body>
</html>'''
