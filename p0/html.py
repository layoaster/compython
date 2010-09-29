# -*- coding: utf-8 -*-
"""
        $Id$
Description: Modulo de creacion de diccionario HTML.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

def head(title = "Untitled", coding = "utf-8"):
    """Cabeceras de html"""
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
    """Enlaza el texto a Google"""
    return u"<a href='http://www.google.es/search?q=" + text + u"'>" + text + u"</a>"

def body(dict):
    table = u"<table border=0>\n"
    sorted = dict.keys()
    sorted.sort()
    char = ""
    for word in sorted:
        if word[0] != char:
            char = word[0]
            table += u"<tr><td>&nbsp;</td></tr>"
            table += u"<tr><td valign=middle colspan=2 style='background: #FFF url(naranja.gif) no-repeat left top'><h3><font color='#FFFFFF'>&nbsp;" + word[0].upper() + u"</font></h3>"
            table += u"</td>\n</tr>\n"
        table += u"<tr>\n<td>" + linkToGoogle(word)
        table += u"&nbsp;&nbsp;&nbsp;</td>\n" + u"<td>"
        for num in dict[word]:
            table += str(num) + u", "
        table = table[:-2]
        table += u"</td>\n</tr>\n"
    return u"<h1>&Iacute;ndice alfab&eacute;tico</h1>\n" + unicode(table) + u"</table>\n"

def tail():
    """Final de html"""
    return u'''
</body>
</html>'''
