#!/bin/zsh
cp=$(print -l jars/*.jar | tr '\n' :)
set -eux
java -cp $cp org.antlr.Tool psf.g

