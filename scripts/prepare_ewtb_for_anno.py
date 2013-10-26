#!/usr/bin/env python2.7
'''
Preprocesses an ARK TweetNLP dataset for GFL annotation.
In the annotation section of each item, the punctuation tokens are removed. 
If a word appears multiple times in a tweet, 
the tokens are indexed with '~1', '~2', etc.

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2013-02-05
'''
from __future__ import print_function
import os, sys, fileinput, re
from collections import Counter

inF = fileinput.input('ewtb55.idtokpos')

PUNCT = [',','.','-LRB-','-RRB-']

try:
	while True:
		ln = next(inF)[:-1]
		itmid,toks,postagged = ln.split('\t')
		print('---')
		print('% ID',itmid)
		print('% POS TEXT')
		print(postagged)

		tkns = []
		tags = []
		c = Counter()
		for tokpos in postagged.split():
			w, tag = tokpos[:tokpos.rindex('/')], tokpos[tokpos.rindex('/')+1:]
			tkn = w
			if tag not in PUNCT:
				c[w] += 1
			tkns.append(tkn)
			tags.append(tag)

		# subscripts for duplicate words
		for w,n in c.items():
			if n>1:
				k = 1
				for i,tkn in enumerate(tkns):
					if tkn.strip()==w:
						tkns[i] = tkn.replace(w, w+'~'+str(k))
						k += 1
				assert k==n+1,(w,n,tkns)

		print()
		print('% TEXT')
		print(' '.join(tkns))
		print('\n% ANNO\n')
		
		print(' '.join((w if tag not in PUNCT else '\n') for w,tag in zip(tkns,tags)).replace('\n ','\n').replace('\n\n','\n'))
		print()
		print()
except StopIteration:
	pass
