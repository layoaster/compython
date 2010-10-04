class Error(Exception):
  def __init__(self):
      pass

class LexicalError(Error):
   _UNKNOWN_CHAR = "Caracter no reconocido"
   _INT_OVERFLOW = "Desbordamiento de entero"
   _UNCLOSED_COM = "Comentario sin cerrar"

   def __init__(self, nline):
      pass
