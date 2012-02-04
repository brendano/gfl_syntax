import antlr3
from psfLexer import psfLexer
from psfParser import psfParser

char_stream = antlr3.ANTLRFileStream('footballwives.txt')

lexer = psfLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = psfParser(tokens)
p = parser.annotate()

def walk(node, indent=0):
  print "{indent} {info}".format(
      indent=' '*(indent*4), 
      info=node.token if node.token else repr(node),
      #s=node.token.text if node.token else ''
      )
  if node.children:
    for c in node.children:
      walk(c, indent=indent+1)

walk(p.tree)

