#!/usr/bin/env python2.7
'''
Evaluation measures for single annotations and for inter-annotator agreement.
'''
from __future__ import print_function, division
import os, re, sys, fileinput, json
from collections import Counter, defaultdict

from graph import FUDGGraph, upward, downward
from spanningtrees import spanning


def single_ann_measures(a):
	c = Counter()
	c['lexnodes'] = len(a.lexnodes)
	c['coordnodes'] = len(a.coordnodes)
	c['FNs'] = len(a.cbbnodes)
	c['explicitly rooted utterances'] = len(a.root.children)
	upward(a)
	downward(a)
	c['possibly rooted utterances'] = len({int('$$' in c.parentcandidates) for c in a.lexnodes})
	return c
	
def iaa_measures(a1,a2):
	pass

def main(anns1F, anns2F=None):
	i = 0
	for ann1ln in anns1F:
		loc1, sent, ann1JS = ann1ln[:-1].split('\t')
		ann1J = json.loads(ann1JS)
		print(i, loc1, '<<', sent)
		a1 = FUDGGraph(ann1J)
		print('   ',single_ann_measures(a1))
		if anns2F is not None:
			ann2ln = next(anns2F)
			loc2, sent2, ann2JS = ann2ln[:-1].split('\t')
			assert sent2==sent
			ann2J = json.loads(ann2JS)
			assert len(ann1J['tokens'])==len(ann2J['tokens'])
			a2 = FUDGGraph(ann2J)
			print(i, loc2, '>>')
			print('   ',single_ann_measures(a2))
			print('   ',iaa_measures(a1,a2))
		i += 1

if __name__=='__main__':
	anns1F = anns2F = None
	if len(sys.argv)>1:
		anns1F = fileinput.input([sys.argv[1]])
		if len(sys.argv)>2:
			anns2F = fileinput.input([sys.argv[2]])
	else:
		anns1F = fileinput.input([])
	main(anns1F,anns2F)
