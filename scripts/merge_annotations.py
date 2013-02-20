#!/usr/bin/env python2.7
#coding=UTF-8
'''
Given two or more parallel outputs of make_json.py for the same sentences, 
merges them into a single annotation to the extent that they are compatible.
Output in the same JSON format as the input.

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2013-02-20
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

def main(annsFF, verbose=False):
	assert len(annsFF)>=2
	
	i = 0
	while True:	# iterate over items
		annsJ = []	# JSON input objects, one per annotator
		mergedJ = None	# JSON output
		anns = []	# FUDG graphs, one per annotator
		locs = []
		
		try:
			for j,annsF in enumerate(annsFF):	# iterate over annotators
				ln = next(annsF)
				loc, sent, annJS = ln[:-1].split('\t')
				locs.append(loc)
				annJ = json.loads(annJS)
				annsJ.append(annJ)
				if verbose: print(i, loc, '<<', sent)
				#a = FUDGGraph(annJ)
				#anns.append(a)
				
				if j==0:
					mergedJ = json.loads(json.dumps(annJ))	# hacky deepcopy
					sent0 = sent
					continue
				
				try:
					assert sent==sent0,(sent0,sent)	# TODO: hmm, why is this failing?
				except AssertionError as ex:
					print(ex, file=sys.stderr)
				
				
				conflictingN2W = {k for k in (set(annJ['node2words'].keys()) & set(mergedJ['node2words'].keys())) if annJ['node2words'][k]!=mergedJ['node2words'][k]}
				assert not conflictingN2W
				
				# TODO: variables/coordination
				conflictingEN2W = {k for k in (set(annJ['extra_node2words'].keys()) & set(mergedJ['extra_node2words'].keys())) if annJ['extra_node2words'][k]!=mergedJ['extra_node2words'][k]}
				assert not conflictingEN2W
				
				# union the ordinary edges
				for e in annJ['node_edges']:
					if e not in mergedJ['node_edges']:
						mergedJ['node_edges'].append(list(e))
				
				# special nodes
				for n in set(annJ['extra_node2words'].keys()) - set(mergedJ['extra_node2words'].keys()):
					mergedJ['extra_node2words'][n] = json.loads(json.dumps(annJ['extra_node2words'][n]))
				
				
				# register any new nodes
				# if there are any multiwords not in all annotations, include them in the merge with the CBBMW prefix
				for n in set(annJ['nodes']) ^ set(mergedJ['nodes']):
					if n.startswith('MW('):
						# multiword not proposed by all annotators. convert to CBBMW
						if n in mergedJ['nodes']:
							mergedJ['nodes'][mergedJ['nodes'].index(n)] = 'CBB'+n
							mergedJ['node2words']['CBB'+n] = mergedJ['node2words'][n]
							del mergedJ['node2words'][n]
						elif 'CBB'+n in mergedJ['nodes']:
							assert mergedJ['node2words']['CBB'+n]==annJ['node2words'][n]
						else:
							mergedJ['nodes'].append('CBB'+n)
							mergedJ['node2words']['CBB'+n] = list(annJ['node2words'][n])
							
						# ensure edges use CBBMW(...)
						for e in mergedJ['node_edges']:
							x,y,lbl = e
							assert x!=y
							if x==n: e[0] = 'CBB'+n
							if y==n: e[1] = 'CBB'+n
							assert e[0]!=e[1]
						for v in mergedJ['extra_node2words'].values():
							for e in v:
								if e[0]==n: e[0] = 'CBB'+n
						
					elif n in annJ['nodes']:
						assert n not in mergedJ['nodes']
						mergedJ['nodes'].append(n)
						if n in annJ['node2words']:
							mergedJ['node2words'][n] = list(annJ['node2words'][n])
			
			output = '|'.join(locs) + '\t' + sent + '\t' + json.dumps(mergedJ)
			
			if verbose:
				print(output, file=sys.stderr)
			
			assert len(set(mergedJ['nodes']))==len(mergedJ['nodes']),'Nodes in input are not unique: '+' '.join(n for n in mergedJ['nodes'] if mergedJ['nodes'].count(n)>1)
			
			try:
				a = FUDGGraph(mergedJ)
				print(output)
				
			except Exception as ex:
				if 'cycle' in ex.message:
					print('CANNOT MERGE',loc,'::',ex, file=sys.stderr)
				else:
					raise
				print()	# blank line--invalid merge!
			
			
			i += 1
			
		except StopIteration:
			break

if __name__=='__main__':
	annsFF = []
	args = sys.argv[1:]
	opts = {}
	
	while args and args[0].startswith('-'):
		opts[{'-v': 'verbose', '-s': 'singleonly'}[args.pop(0)]] = True
	
	assert len(args)>=2
	
	while args:
		annsF = fileinput.input([args.pop(0)])
		annsFF.append(annsF)
	
	main(annsFF,**opts)
