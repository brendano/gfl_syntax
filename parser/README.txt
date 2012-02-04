To compile the grammar, you will need ANTLR v3 (http://www.antlr.org/).

To compile the grammar:
  ./build.sh

To run it:
  python python-driver.py

For development, I've been using ANTLRWorks which is also available
from the ANTLR website.

DOT visualization of parse tree
-------------------------------
  # compile psf grammar into java
  java -cp jars/antlr-3.4-complete.jar org.antlr.Tool psf.g

  # compile java tool and generated compilers
  javac -cp jars/antlr-3.4-complete.jar AnnotationTreeToDOT.java psfParser.java psfLexer.java

  # run 
  ../anno_code/strip_preamble.pl ../anno/dev.0000.anno | java -cp jars/antlr-3.4-complete.jar:. AnnotationTreeToDOT > dev0000.dot

  # display, e.g.:
  dotty dev0000.dot

