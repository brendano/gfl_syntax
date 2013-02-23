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
from measures import promcom, single_ann_measures

def main(annsFF, verbose=False, simplifycoords=False):
	assert len(annsFF)>=2
	
	i = 0
	allC = Counter()
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
				if verbose: print(i, loc, '<<', sent, file=sys.stderr)
				#a = FUDGGraph(annJ)
				#anns.append(a)
				
				if simplifycoords:
					aX = FUDGGraph(annJ)
					simplify_coord(aX)
					annsJ[-1] = annJ = aX.to_json_simplecoord()
					if verbose: print(annJ, file=sys.stderr)
				
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
				'''
				conflictingEN2W = {k for k in (set(annJ['extra_node2words'].keys()) & set(mergedJ['extra_node2words'].keys())) if annJ['extra_node2words'][k]!=mergedJ['extra_node2words'][k]}
				for k in conflictingEN2W:
					annJ['extra_node2words'][k+'_'] = annJ['extra_node2words'][k]	# TODO: Hacky
					del annJ['extra_node2words'][k]
					annJ['nodes'][annJ['nodes'].index(k)] = k+'_'
					for e in annJ['node_edges']:
						x,y,lbl = e
						if x==k: e[0] = k+'_'
						if y==k: e[1] = k+'_'
				print(annJ)
				'''
				conflictingEN2W = {k for k in (set(annJ['extra_node2words'].keys()) & set(mergedJ['extra_node2words'].keys())) if annJ['extra_node2words'][k]!=mergedJ['extra_node2words'][k]}
				assert not conflictingEN2W,conflictingEN2W
					
				
				# union the ordinary edges
				for e in annJ['node_edges']:
					if e not in mergedJ['node_edges']:
						mergedJ['node_edges'].append(list(e))
				
				# special nodes
				for n in set(annJ['extra_node2words'].keys()) - set(mergedJ['extra_node2words'].keys()):
					mergedJ['extra_node2words'][n] = json.loads(json.dumps(annJ['extra_node2words'][n]))
				
				
				# register any new nodes
				# if there are any multiwords not in all annotations, include them in the merge with the CBBMW prefix
				for n in sorted(set(annJ['nodes']) ^ set(mergedJ['nodes']), reverse=True):	# reverse lexicographic sorting puts CBBMW after MW O_O
					#print(n, mergedJ['nodes'], file=sys.stderr)
					if n.startswith('MW('):
						# multiword not proposed by all annotators. convert to CBBMW
						if n in mergedJ['nodes']:
							mergedJ['nodes'][mergedJ['nodes'].index(n)] = 'CBB'+n
							mergedJ['node2words']['CBB'+n] = mergedJ['node2words'][n]
							del mergedJ['node2words'][n]
						elif 'CBB'+n in mergedJ['nodes']:
							assert mergedJ['node2words']['CBB'+n]==annJ['node2words'][n]
						else:
							assert 'CBB'+n not in mergedJ['nodes']
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
					#elif n.startswith('CBBMW(') and n in annJ['nodes']:
					#	# convert to CBBMW for this annotator
					#	pass	# TODO: ?
					#elif n.startswith('CBBMW(') and n in mergedJ['nodes']:
					#	assert False	# TODO?
					elif n in annJ['nodes'] and n not in mergedJ['nodes']:
						if n.startswith('W('):	# ensure single word is not already covered by a (CBB)MW
							tkn = n[2:-1]
							if any(tkn in tkns for tkns in mergedJ['node2words'].values()):
								continue
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
				try:
					c = single_ann_measures(a)
					if verbose: print(c, file=sys.stderr)
					allC += c
				except Exception as ex:
					print('CANNOT EVALUATE MERGE',loc,'::',ex, file=sys.stderr)
					allC['invalid'] += 1
				
			except Exception as ex:
				if 'cycle' in ex.message:
					print('CANNOT MERGE',loc,'::',ex, file=sys.stderr)
				else:
					raise
				print()	# blank line--invalid merge!
			
			
			i += 1
			
		except StopIteration:
			break

	print(allC, file=sys.stderr)

if __name__=='__main__':
	annsFF = []
	args = sys.argv[1:]
	opts = {}
	
	while args and args[0].startswith('-'):
		opts[{'-v': 'verbose', '-s': 'singleonly', '-c': 'simplifycoords'}[args.pop(0)]] = True
	
	assert len(args)>=2
	
	while args:
		annsF = fileinput.input([args.pop(0)])
		annsFF.append(annsF)
	
	main(annsFF,**opts)
