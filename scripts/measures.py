#!/usr/bin/env python2.7
#coding=UTF-8
'''
Evaluation measures for single annotations and for inter-annotator agreement.
'''
from __future__ import print_function, division
import os, re, sys, fileinput, json, math
from collections import Counter, defaultdict

from graph import FUDGGraph, simplify_coord, upward, downward
from spanningtrees import spanning

class ValueStats(object):
	def __init__(self, val=None, show=None):
		self.instances = Counter()
		self.show = show
		if val is not None:
			self += val
	def __add__(self, val):
		if isinstance(val,ValueStats):
			self.instances += val.instances
		else:
			self.instances[val] += 1
		return self
	@property
	def sum_n_mean_median_mode(self):
		elts = tuple(self.instances.elements())
		#assert False,list(elts)
		try:
			tot = sum(elts)
		except:
			print(list(elts))
			raise
		n = len(elts)
		mean = tot/n
		med = .5*(elts[len(elts)//2-1]+elts[len(elts)//2]) if len(elts)%2==0 else elts[len(elts)//2+1]
		mode = self.instances.most_common(1)[0][0]
		return tot, n, mean, med, mode
	@property
	def power_threshold_histogram(self):
		c = Counter()
		c['0'] = self.instances[0]
		c['1'] = self.instances[1]
		c[    '>=2'] = sum(v for k,v in self.instances.items() if k>=2)
		c[   '>=10'] = sum(v for k,v in self.instances.items() if k>=10)
		c[  '>=100'] = sum(v for k,v in self.instances.items() if k>=100)
		c[ '>=1000'] = sum(v for k,v in self.instances.items() if k>=1000)
		c['>=10000'] = sum(v for k,v in self.instances.items() if k>=10000)
		return c
	def __str__(self):
		if not self.instances: return 'ValueStats()'	# empty
		elif sum(self.instances.values())==1:
			return str(self.instances.most_common(1)[0][0])
		elif self.show=='mean':
			return '[mean={}]'.format(self.sum_n_mean_median_mode[2])
		return '[min={} max={} mean={}/{}={} med={} mode={}]'.format(min(self.instances.keys()),
															  max(self.instances.keys()),
															  *self.sum_n_mean_median_mode) + str(self.power_threshold_histogram)
	def __repr__(self):
		return str(self)

def parentmap(edges):
	return {v:u for u,v in edges}	# assumes edges is a tree with (parent,child) pairs!

def depth(v, parmap):
	if parmap[v] not in parmap: return 0
	return 1+depth(parmap[v],parmap)


def promcom(a, c):
	def compatible_analyses(spanning_trees, nodeswithext):
		for analysis in spanning_trees:
			parmap = parentmap(analysis)
			#assert False,parmap
			violation = False

			# determine tops of all CBBs in this analysis, going upward
			tops = {}
			for cbb in sorted(a.cbbnodes, key=lambda node: node.height):
				tops[cbb.name] = min((tops.get(n.name,n.name) for n in cbb.members), key=lambda v: depth(v,parmap))

			for cbb in nodeswithext:
				top = tops[cbb.name]
				for x in cbb.externalchildren:
					if (parmap.get(x.name) or parmap[tops[x.name]])!=top:
						violation = True
						#if 'tix' in a.alltokens:
						#	assert False,(tops,x.name,parmap.get(x.name) or parmap[tops[x.name]],top,analysis)
						break
				if violation: break
			if not violation:
				yield analysis

	stg = {(p.name,n.name) for n in a.lexnodes for p in n.parentcandidates}
	#print(stg)
	try:
		strees = spanning(stg, '$$', threshold=20000)
		assert len(strees)>0
		c['spanning trees'] = ValueStats(len(strees))
		nodeswithext = {cbb for cbb in a.cbbnodes if cbb.externalchildren}
		prom = sum(1 for t in compatible_analyses(strees, nodeswithext))
		assert prom>0,'No compatible trees for sentence: '+' '.join(a.alltokens)
		c['promiscuity'] = ValueStats(prom)
		N = len(a.lexnodes)+1
		assert N>=2
		com = 1-math.log(prom)/((N-2)*math.log(N)) if N>2 else prom
		c['commitment'] = ValueStats(com, show='mean')

	except Exception as ex:
		if ex.message=='Too many spanning trees.':
			c['spanning tree overflow'] += 1
			c['spanning trees'] = ValueStats()	# prevents this from being counted (otherwise registers as 0)
			c['promiscuity'] = ValueStats()
			c['commitment'] = ValueStats()	# TODO: ??
		else:
			raise

def single_ann_measures(a):
	c = Counter()
	c['lexnodes'] = len(a.lexnodes)
	c['1W'] = sum(1 for n in a.lexnodes if len(n.tokens)==1)
	c['MW'] = sum(1 for n in a.lexnodes if len(n.tokens)>1)
	c['omittedtoks'] = len(a.alltokens)-sum(1 for n in a.lexnodes)
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
	c['possible utterance heads'] = sum(int(a.root in n.parentcandidates) for n in a.lexnodes)
	promcom(a,c)

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
