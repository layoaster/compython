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
        a:link {text-decoration:none; color: #079af0;}
        a:visited {text-decoration:none; color:#0d4fbf}
        a:active {text-decoration:none; color:#0d4fbf; background:#EEEEEE}
        a:hover {text-decoration:underline; color:#82562e; background: #EEEEEE}
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
    char = " "
    for word in sorted:
        if word[0] != char:
            char = word[0]
            table += "<tr><td>&nbsp;</td></tr>"
            table += "<tr><td valign=middle colspan=2 style='background: #FFF url(naranja.gif) no-repeat left top'><h3><font color='#FFFFFF'>&nbsp;" + word[0].upper() + "</font></h3>"
            table += "</td>\n</tr>\n"
        table += "<tr>\n<td>" + linkToGoogle(word)
        table += "&nbsp;&nbsp;&nbsp;</td>\n" + "<td>"
        for num in dict[word]:
            table += str(num) + ", "
        table = table[:-2]
        table += "</td>\n</tr>\n"
    return "<h1>&Iacute;ndice alfab&eacute;tico</h1>\n" + table + "</table>\n"

def tail():
    """Final de html"""
    return '''
</body>
</html>'''
