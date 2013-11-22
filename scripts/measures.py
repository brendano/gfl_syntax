#!/usr/bin/env python2.7
#coding=UTF-8
'''
Evaluation measures for single annotations and for inter-annotator agreement.
'''
from __future__ import print_function, division
import os, re, sys, fileinput, json, math
from collections import Counter, defaultdict

from graph import FUDGGraph, LexicalNode, simplify_coord, upward, downward
from spanningtrees import spanning
from kirchhoff import spanningtree
from merge_annotations import *

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
	def __float__(self):
		if sum(self.instances.values())==1:
			return float(self.instances.keys()[0])
		assert sum(self.instances.values())==0
		return float('nan')
		
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
		c[     '<1'] = sum(v for k,v in self.instances.items() if k<1)
		c['1'] = self.instances[1]
		c[     '>1'] = sum(v for k,v in self.instances.items() if k>1)
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

def com(prom, N):
	com = 1-math.log(prom)/((N-2)*math.log(N)) if N>2 else prom
	if abs(com) < 1e-10:
		com = 0
	if N==2: assert prom in (0,1)
	assert 0.0<=com<=1.0,(com,prom,N)
	return com

def promcom(a, c, kirchhoff=False):
	stg = {(p.name,n.name) for n in a.lexnodes for p in n.parentcandidates}
	#stg = {(p.name,n.name) for n in a.nodes-{a.root} for ch in (n.topcandidates if n.isFE else {n.name}) for p in n.parentcandidates}
	assert any(1 for x,y in stg if x=='**'),('The root ** is not in the graph!',stg)

	if kirchhoff:	# approximate promiscuity: count spanning trees with matrix tree theorem (instead of enumerating them). an upper bound.
		prom = spanningtree(stg, '**')
		c['spanning trees'] = ValueStats(prom)
		if prom==0:
			raise Exception('No spanning trees for: '+repr(stg))
		c['promiscuity'] = ValueStats(prom)
		N = len(a.lexnodes)+1
		assert N>=2
		c['commitment'] = ValueStats(com(prom,N), show='mean')
		return

	def compatible_analyses(spanning_trees, nodeswithext):
		for analysis in spanning_trees:
			parmap = parentmap(analysis)
			#assert False,parmap
			violation = False

			# determine tops of all FEs in this analysis, going upward
			tops = {}
			for fe in sorted(a.fenodes, key=lambda node: node.height):
				assert fe.members,(fe,fe._pointerto)
				tops[fe.name] = min((tops.get(n.name,n.name) for n in fe.members), key=lambda v: depth(v,parmap))

			for fe in nodeswithext:
				top = tops[fe.name]
				for x in fe.externalchildren:
					if (parmap.get(x.name) or parmap[tops[x.name]])!=top:
						violation = True
						#if 'tix' in a.alltokens:
						#	assert False,(tops,x.name,parmap.get(x.name) or parmap[tops[x.name]],top,analysis)
						break
				if violation: break
			if not violation:
				yield analysis
	
	try:
		strees = spanning(stg, '**', threshold=10000)
		assert len(strees)>0
		c['spanning trees'] = ValueStats(len(strees))
		nodeswithext = {fe for fe in a.fenodes if fe.externalchildren}
		prom = sum(1 for t in compatible_analyses(strees, nodeswithext))
		assert prom>0,'No compatible trees for sentence: '+' '.join(a.alltokens)
		c['promiscuity'] = ValueStats(prom)
		N = len(a.lexnodes)+1
		assert N>=2
		c['commitment'] = ValueStats(com(prom,N), show='mean')
	except Exception as ex:
		if ex.message=='Too many spanning trees.':
			c['spanning tree overflow'] += 1
			c['spanning trees'] = ValueStats()	# prevents this from being counted (otherwise registers as 0)
			c['promiscuity'] = ValueStats()
			c['commitment'] = ValueStats()	# TODO: ??
		elif 'No compatible trees' in ex.message:
			raise
		else:
			raise Exception('No spanning trees for: '+repr(stg))

def iapromcom(a1, a2, c, escapebrackets=False, kirchhoff=False):
	'''
	Measures local compatibility of constraints in two annotations.
	Assumes single_ann_measures() has already been run independently on the two annotation graphs.
	See merge_annotations.py to measure global compatibility of two annotations (i.e. reasoning over the entire structure).
	'''
	a1J, a2J = a1.to_json_simplecoord(), a2.to_json_simplecoord()
	#print()
	#print(a1J)
	#print()
	#print(a2J)
	m = merge([a1J, a2J], updatelex=True, escapebrackets=escapebrackets)
	a1U = FUDGGraph(a1J)
	a2U = FUDGGraph(a2J)
	upward(a1U)
	downward(a1U)
	upward(a2U)
	downward(a2U)
	for n in a1U.lexnodes | a2U.lexnodes:
		assert n.json_name in a1U.nodesbyname,(n.json_name,m,'-------------------',a1J)
		assert n.json_name in a2U.nodesbyname,(n.json_name,m,'-------------------',a2J)
		#assert n.json_name in m['node2words'] or (n.json_name.startswith('MW(') and 'FE'+n.json_name in m['node2words']),(n.json_name,m)

	jointSuppParents = {n.name: {p.json_name for p in a1U.nodesbyname[n.json_name].parentcandidates} & {p.json_name for p in a2U.nodesbyname[n.json_name].parentcandidates} for n in (a1U.lexnodes|a2U.lexnodes)}
	
	# compute single-annotation commitment (w/ compatible lexical level)
	a1C, a2C = Counter(), Counter()
	promcom(a1U, a1C, kirchhoff=kirchhoff)
	promcom(a2U, a2C, kirchhoff=kirchhoff)
	a1com, a2com = a1C['commitment'], a2C['commitment']
	#if float(a2com)<1 and '"~2' not in a2U.alltokens:
	#	promcom(a2U, a2C, kirchhoff=kirchhoff, debug=True)
	#	assert False,(a2U.alltokens,a2C,a2.lexnodes)
	
	numer = sum(len(jointpars) for jointpars in jointSuppParents.values())
	c['softprec_1|2'] = ValueStats(numer/sum(len(n.parentcandidates) for n in a1U.lexnodes))
	c['softprec_2|1'] = ValueStats(numer/sum(len(n.parentcandidates) for n in a2U.lexnodes))
	if math.isnan(float(a1com)) or math.isnan(float(a2com)):
		assert a1C['spanning tree overflow'] or a2C['spanning tree overflow'],('internally inconsistent:', a1C if math.isnan(float(a1com)) else a2C)
		c['a1com'] = ValueStats()
		c['a2com'] = ValueStats()
		c['softcomprec_1|2'] = ValueStats()
		c['softcomprec_2|1'] = ValueStats()
		c['softcomprec_discarded'] = 1
		c['too_many_spanning_trees'] = 1
		c['comprec_1|2'] = ValueStats()
		c['comprec_2|1'] = ValueStats()
		return
	else:
		assert 0.0<=float(a1com)<=1.0,float(a1com)
		assert 0.0<=float(a2com)<=1.0,float(a2com)
		c['a1com'] = ValueStats(a1com)
		c['a2com'] = ValueStats(a2com)
		c['softcomprec_1|2'] = ValueStats(float(a1com)*float(c['softprec_1|2']))
		c['softcomprec_2|1'] = ValueStats(float(a2com)*float(c['softprec_2|1']))
	
	try:
		ma = FUDGGraph(m)
		try:
			upward(ma)
			downward(ma)
			maC = Counter()
			try:
				promcom(ma, maC, kirchhoff=kirchhoff)
				maprom = maC['promiscuity']
				macom = maC['commitment']
				c['comprec_1|2'] = ValueStats(float(macom)*float(maprom)/float(a1C['promiscuity']))
				c['comprec_2|1'] = ValueStats(float(macom)*float(maprom)/float(a2C['promiscuity']))
				c['comprec_nonzero'] = 1
			except Exception as ex:
				c['comprec_1|2'] = ValueStats(0)
				c['comprec_2|1'] = ValueStats(0)
				print('~',ex, file=sys.stderr)
				print(' '.join(a1.alltokens)+'\n', file=sys.stderr)
				if 'No spanning trees' in ex.message:
					c['no_spanning_trees'] = 1
				elif 'No compatible trees' in ex.message:
					c['no_compatible_trees'] = 1	# due to external-attachment-to-FE constraint
				else:
					print('unknown error in promcom()', file=sys.stderr)
					raise
		except Exception as ex:
			c['comprec_1|2'] = ValueStats(0)
			c['comprec_2|1'] = ValueStats(0)
			print('~',ex, file=sys.stderr)
			print(' '.join(a1.alltokens)+'\n', file=sys.stderr)
			if 'any possible heads' in ex.message:
				c['empty_spanning_tree_graph'] = 1
			else:
				raise
	except Exception as ex:
		c['comprec_1|2'] = ValueStats(0)
		c['comprec_2|1'] = ValueStats(0)
		print('~',ex, file=sys.stderr)
		print(' '.join(a1.alltokens)+'\n', file=sys.stderr)
		if 'cycle' in ex.message:
			c['merge_cycle'] = 1
		elif 'specified top' in ex.message:
			c['merge_extra_top'] = 1
		else:
			raise
		c['no_valid_merge'] = 1
	

def single_ann_measures(a, kirchhoff=False):
	c = Counter()
	c['lexnodes'] = len(a.lexnodes)
	c['1W'] = sum(1 for n in a.lexnodes if len(n.tokens)==1)
	c['MW'] = sum(1 for n in a.lexnodes if len(n.tokens)>1)
	c['omittedtoks'] = len(a.alltokens)-sum(len(n.tokens) for n in a.lexnodes)
	c['coordnodes'] = len(a.coordnodes)
	c['anaphlinks'] = len(a.anaphlinks)
	c['FNs'] = len(a.fenodes)
	c['explicitly rooted utterances'] = len(a.root.children)
	#print({n: n.depth for n in a.nodes})
	simplify_coord(a)
	c['projective'] = int(a.isProjective)
	# literal number of connected components in the graph (not counting the root when nothing was explicitly attached to it)
	c['fragments'] = len({n.frag for n in a.nodes if n.frag.nodes!={a.root}})
	assert c['fragments']>0,(a.nodes,a.lexnodes)
	c['max utterances'] = max(1,c['explicitly rooted utterances'])+(c['fragments']-1)
	c['min utterances'] = max(1,c['explicitly rooted utterances'])
	assert c['max utterances']>=c['min utterances'],c
	upward(a)
	downward(a)
	c['possible utterance heads'] = sum(int(a.root in n.parentcandidates) for n in a.lexnodes)
	promcom(a,c, kirchhoff=kirchhoff)

	return c
	
def iaa_measures(a1,a2, escapebrackets=False, kirchhoff=False):
	c = Counter()
	iapromcom(a1,a2,c, escapebrackets=escapebrackets, kirchhoff=kirchhoff)
	return c

def main(anns1F, anns2F=None, verbose=False, escapebrackets=False, kirchhoff=False):
	i = 0
	a1C, a2C, iaC = Counter(), Counter(), Counter()
	for ann1ln in anns1F:
		if not ann1ln.strip(): continue
		loc1, sent, ann1JS = ann1ln[:-1].split('\t')
		ann1J = json.loads(ann1JS)
		if verbose: sys.stderr.flush(); print(i, loc1, '<<', sent); sys.stdout.flush()
		a1 = FUDGGraph(ann1J)
		a1single = single_ann_measures(a1, kirchhoff=kirchhoff)
		a1C += a1single
		if verbose: print('   ',a1single)
		if anns2F is not None:
			ann2ln = next(anns2F)
			if not ann2ln.strip(): continue
			loc2, sent2, ann2JS = ann2ln[:-1].split('\t')
			#assert sent2==sent,(sent,sent2)
			ann2J = json.loads(ann2JS)
			assert len(ann1J['tokens'])==len(ann2J['tokens'])
			#assert ann1J['tokens']==ann2J['tokens'],(ann1J['tokens'],ann2J['tokens'])
			a2 = FUDGGraph(ann2J)
			if verbose: sys.stderr.flush(); print(i, loc2, '>>', sent2); sys.stdout.flush()
			a2single = single_ann_measures(a2, kirchhoff=kirchhoff)
			a2C += a2single
			if verbose: print('   ',a2single)
			iaa = iaa_measures(a1,a2, escapebrackets=escapebrackets, kirchhoff=kirchhoff)
			iaC += iaa
			if verbose: print('   ',iaa)
		i += 1
	if verbose: print()
	print(a1C)
	if a2C:
		print()
		print(a2C)
		print()
		print('INTER-ANNOTATOR:')
		print(iaC)

if __name__=='__main__':
	anns1F = anns2F = None
	args = sys.argv[1:]
	opts = {}
	
	while args and args[0].startswith('-'):
		opts[{'-v': 'verbose', '-s': 'singleonly', '-b': 'escapebrackets', '-k': 'kirchhoff'}[args.pop(0)]] = True
	
	if not args:
		anns1F = fileinput.input([])
	else:
		if not opts.get('singleonly'):
			anns1F = fileinput.input([args.pop(0)])
			assert len(args)<=2,'Too many arguments'
			if args:
				anns2F = fileinput.input([args.pop(0)])
	
	if opts.get('singleonly'):
		del opts['singleonly']
		while True:
			anns1F = fileinput.input([args.pop(0)])
			main(anns1F,**opts)
			if not args:
				break
	else:	# if there are two arguments, compare the two annotations
		main(anns1F,anns2F,**opts)
