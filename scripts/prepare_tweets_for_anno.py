#!/usr/bin/env python2.7
'''
Preprocesses an ARK TweetNLP dataset for GFL annotation.
In the annotation section of each item, the sentence is split on 
punctuation tokens, emoticons, and interjections, and then 
the punctuation tokens are removed. If a word appears multiple times in a tweet, 
the tokens are indexed with '~1', '~2', etc.

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2013-02-05
'''
from __future__ import print_function
import os, sys, fileinput, re
from collections import Counter

inF = fileinput.input('twpos-data-v0.3/full_data/daily547.supertsv')

try:
	while True:
		ln = next(inF)[:-1]
		assert ln.startswith('TWEET\t'),repr(ln)
		itmid = ln.split('\t')[1]
		ln = next(inF)[:-1]
		assert ln=='TOKENS'
		print('---')
		print('% ID',itmid)
		print('% POS TEXT')
		ww = []
		c = Counter()
		for ln in inF:
			ln=ln[:-1]
			if not ln:
				break
			tag, w = ln.split('\t')
			tkn = w
			print(tkn, tag, sep='/', end=' ')
			if tag in ('!','E'):	# always separate interjections and emoticons
				tkn = '\n'+tkn+'\n'
			if re.search(r'^[.,!?:*]+$', tkn) is None:
				c[w] += 1
				
			ww.append(tkn)

		# subscripts for duplicate words
		for w,n in c.items():
			if n>1:
				k = 1
				for i,tkn in enumerate(ww):
					if tkn.strip()==w:
						ww[i] = tkn.replace(w, w+'~'+str(k))
						k += 1
				assert k==n+1,(w,n,ww)

		print()
		print('% TEXT')
		print(' '.join(ww).replace('\n',''))
		print('\n% ANNO\n')
		
		s1 = ' '.join(['']+ww+['']).replace('\n',' \n ')
		s = re.sub(r' [.,!?:*]+?(?=\s)', ' \n ', s1)
		assert '...' not in s,(s1,s)
		s = re.sub(r'\n([ ]*\n)+', '\n', s)
		s = re.sub(r'\n[ ]*', '\n', s)
		print(s.strip())
		print()
		print()
except StopIteration:
	pass
