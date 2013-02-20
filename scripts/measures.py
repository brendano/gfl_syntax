#!/usr/bin/env python2.7
'''
Evaluation measures for single annotations and for inter-annotator agreement.
'''
from __future__ import print_function, division
import os, re, sys, fileinput, json
from collections import Counter, defaultdict

from graph import FUDGGraph, simplify_coord, upward, downward
from spanningtrees import spanning


def single_ann_measures(a):
	c = Counter()
	c['lexnodes'] = len(a.lexnodes)
	c['1W'] = sum(1 for n in a.lexnodes if len(n.tokens)==1)
	c['MW'] = sum(1 for n in a.lexnodes if len(n.tokens)>1)
	c['coordnodes'] = len(a.coordnodes)
	c['anaphlinks'] = len(a.anaphlinks)
	c['FNs'] = len(a.cbbnodes)
	c['explicitly rooted utterances'] = len(a.root.children)
	#print({n: n.depth for n in a.nodes})
	simplify_coord(a)
	# literal number of connected components in the graph (not counting the root when nothing was explicitly attached to it)
	c['fragments'] = len({n.frag for n in a.nodes if n.frag.nodes!={a.root}})
	assert c['fragments']>0,(a.nodes,a.lexnodes)
	c['max utterances'] = max(1,c['explicitly rooted utterances'])+(c['fragments']-1)
	c['min utterances'] = max(1,c['explicitly rooted utterances'])
	assert c['max utterances']>=c['min utterances'],c
	upward(a)
	downward(a)
	c['possible utterance heads'] = sum(int(a.root in c.parentcandidates) for c in a.lexnodes)
	return c
	
def iaa_measures(a1,a2):
	pass

def main(anns1F, anns2F=None):
	i = 0
	a1C, a2C, iaC = Counter(), Counter(), Counter()
	for ann1ln in anns1F:
		loc1, sent, ann1JS = ann1ln[:-1].split('\t')
		ann1J = json.loads(ann1JS)
		print(i, loc1, '<<', sent)
		a1 = FUDGGraph(ann1J)
		a1single = single_ann_measures(a1)
		a1C += a1single
		print('   ',a1single)
		if anns2F is not None:
			ann2ln = next(anns2F)
			loc2, sent2, ann2JS = ann2ln[:-1].split('\t')
			assert sent2==sent
			ann2J = json.loads(ann2JS)
			assert len(ann1J['tokens'])==len(ann2J['tokens'])
			a2 = FUDGGraph(ann2J)
			print(i, loc2, '>>')
			a2single = single_ann_measures(a2)
			a2C += a2single
			print('   ',a2single)
			iaa = iaa_measures(a1,a2)
			iaC += iaa
			print('   ',iaa)
		i += 1
	print()
	print(a1C)
	if a2C:
		print(a2C)
		print(iaC)

if __name__=='__main__':
	anns1F = anns2F = None
	if len(sys.argv)>1:
		anns1F = fileinput.input([sys.argv[1]])
		if len(sys.argv)>2:
			anns2F = fileinput.input([sys.argv[2]])
	else:
		anns1F = fileinput.input([])
	main(anns1F,anns2F)
