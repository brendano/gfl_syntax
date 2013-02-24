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
from measures import *

def mw2CBBMW(ann, n):
	'''Given the JSON object for an annotation and the name of a MW node, convert it to a CBBMW node'''
	assert n.startswith('MW(')
	assert n in ann['nodes'],(n,ann['nodes'])
	assert 'CBB'+n not in ann['nodes']
	
	ann['nodes'][ann['nodes'].index(n)] = 'CBB'+n
	ann['node2words']['CBB'+n] = ann['node2words'][n]
	del ann['node2words'][n]
	
	# create single-word tokens
	for tkn in ann['node2words']['CBB'+n]:
		if 'W('+tkn+')' not in ann['nodes']:	# may already be there due to an overlapping CBBMW
			ann['nodes'].append('W('+tkn+')')
			ann['node2words']['W('+tkn+')'] = [tkn]
	
	# ensure edges use CBBMW(...)
	for e in ann['node_edges']:
		x,y,lbl = e
		assert x!=y
		if x==n: e[0] = 'CBB'+n
		if y==n: e[1] = 'CBB'+n
		assert e[0]!=e[1]
	for v in ann['extra_node2words'].values():
		for e in v:
			if e[0]==n: e[0] = 'CBB'+n


def merge(annsJ, updatelex=False, escapebrackets=False):

	for j,annJ in enumerate(annsJ):
	
				
	
				#print(j,file=sys.stderr)
				lexnodes = {n for n in annJ['nodes'] if 'W(' in n}	# excluding root
				assert set(annJ['node2words'].keys())==lexnodes,('Mismatch between nodes and node2words in input',j,lexnodes^set(annJ['node2words'].keys()),annJ)
				
				# normalize tokens: bracket escaping
				if escapebrackets:
					ESCAPES = {'(': '_LRB_', ')': '_RRB_', '<': '_LAB_', '>': '_RAB_', '[': '_LSB_', ']': '_RSB_', '{': '_LCB_', '}': '_RCB_'}
					for i,tkn in enumerate(annJ['tokens']):
						if re.search('|'.join(re.escape(k) for k in ESCAPES.keys()), tkn):
							assert updatelex
							for k,v in ESCAPES.items():
								annJ['tokens'][i] = annJ['tokens'][i].replace(k,v)
				
				if j==0:
					mergedJ = json.loads(json.dumps(annJ))	# hacky deepcopy
					continue
				
				# normalize tokens: indexing
				# some tokens may not be tilde-indexed in all annotations
				# note that if a token is repeated, it cannot have been used in the graph; 
				# so there is no need to update nodes/edges when adding tilde indices
				assert len(annJ['tokens'])==len(mergedJ['tokens'])
				if annJ['tokens']!=mergedJ['tokens']:
					missing = set(enumerate(mergedJ['tokens']))-set(enumerate(annJ['tokens']))
					repeated = {(i,wtype) for i,wtype in missing if mergedJ['tokens'].count(wtype)>1}
					for i,wtype in repeated:
						assert annJ['tokens'][i][:annJ['tokens'][i].rindex('~')]==wtype
						assert annJ['tokens'][i] not in mergedJ['tokens']
						mergedJ['tokens'][i] = annJ['tokens'][i]
						if updatelex:
							for ann in annsJ[:-1]:
								ann['tokens'][i] = mergedJ['tokens'][i]
					
					extra = set(enumerate(annJ['tokens']))-set(enumerate(mergedJ['tokens']))
					repeated = {(i,wtype) for i,wtype in extra if annJ['tokens'].count(wtype)>1}
					for i,wtype in repeated:
						assert updatelex
						assert mergedJ['tokens'][i][:mergedJ['tokens'][i].rindex('~')]==wtype
						assert mergedJ['tokens'][i] not in annJ['tokens']
						annJ['tokens'][i] = mergedJ['tokens'][i]
							
					print('After attempting to reconcile tilde indices:',annJ['tokens'],mergedJ['tokens'],file=sys.stderr)
					
					assert annJ['tokens']==mergedJ['tokens']
				
				
				# TODO: smart renaming of conflicting CBBs?
				conflictingN2W = {k for k in (set(annJ['node2words'].keys()) & set(mergedJ['node2words'].keys())) if annJ['node2words'][k]!=mergedJ['node2words'][k]}
				assert not conflictingN2W
				
				# TODO: smart renaming of conflicting variables?
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
				# include in the merge the union of all single-word nodes not represented by a CBBMW

				for q in range(2 if updatelex else 1):	# repeat in case a CBBMW is introduced in the first iteration, necessitating new W nodes

					# newly encountered lexical nodes
					for n in set(annJ['nodes']) - set(mergedJ['nodes']):
						if n.startswith('MW('):	# this annotation has MW, the merge doesn't, so make it a CBBMW
							if 'CBB'+n not in mergedJ['nodes']:	# merge doesn't have a CBBMW, so make one
								if n in mergedJ['nodes']:	# merge has MW
									assert False,'I think this is outdated code, should never be reached'
									mw2CBBMW(mergedJ, n)
									if updatelex:
										for ann in annsJ[:-1]:
											if n in ann['nodes']:
												mw2CBBMW(ann, n)
								else:	# merge had/has single-words only (or perhaps, overlapping (CBB)MWs?)	# TODO: overlap case? CBBMW that is the union of overlapping MWs?
										# single-words would have been removed at the beginning of the loop
										# slightly hacky: add MW, then convert it to CBBMW (this also converts the edges)
									for ann in [mergedJ]+(annsJ[:-1] if updatelex else []):
										ann['nodes'].append(n)
										ann['node2words'][n] = list(annJ['node2words'][n])
										mw2CBBMW(ann, n)

							if updatelex:
									mw2CBBMW(annJ, n)
						elif n.startswith('CBBMW(') and n[3:] in mergedJ['nodes']:
							# this annotation has CBBMW, merge has MW
							for ann in [mergedJ]+(annsJ[:-1] if updatelex else []):
								mw2CBBMW(ann, n[3:])
						else:
							assert n.startswith('CBB') or n.startswith('W(') or n.startswith('$'),n
						
							considerupdating = [mergedJ] + (annsJ[:-1] if updatelex and n.startswith('W(') else [])
							for ann in considerupdating:
								if n in ann['nodes']: continue
								if n.startswith('W('):	# ensure single word is not already covered by a MW (CBBMW is OK)
									if any(lexnode.startswith('MW(') and n[2:-1] in tkns for lexnode,tkns in ann['node2words'].items()):
										continue
								elif n.startswith('CBBMW('):	# do not add a CBBMW if it overlaps with an MW
									cbbmwtkns = annJ['node2words'][n]
									if any(lexnode.startswith('MW(') and set(cbbmwtkns)&set(mwtkns) for lexnode,mwtkns in ann['node2words'].items()):
										continue
								ann['nodes'].append(n)
								if n in annJ['node2words']:
									ann['node2words'][n] = list(annJ['node2words'][n])
							'''
							if n.startswith('W('):	# ensure single word is not already covered by a MW (CBBMW is OK)
								tkn = n[2:-1]
								if any(lexnode.startswith('MW(') and tkn in tkns for lexnode,tkns in mergedJ['node2words'].items()):
									continue
							#assert n!='W($$)'
							mergedJ['nodes'].append(n)
							if n in annJ['node2words']:
								mergedJ['node2words'][n] = list(annJ['node2words'][n])
							if n.startswith('W(') and updatelex:
								for ann in annsJ[:-1]:
									ann['nodes'].append(n)
									ann['node2words'][n] = list(annJ['node2words'][n])
							'''
				
					# lexical items in the merge of previous annotations, but not this one
					# note that the merge can acquire single-word nodes not in either annotation 
					# if a MW from one of the annotations is converted to a CBBMW in the merge!
					for n in set(mergedJ['nodes']) - set(annJ['nodes']):
						if n.startswith('MW('):
							# in the merge, relax MW to a CBBMW
							mw2CBBMW(mergedJ, n)
							newcbbmmw = True
							if updatelex:
								for ann in annsJ[:-1]:
									if n in ann['nodes']:
										mw2CBBMW(ann, n)
						else:
							assert n.startswith('CBB') or n.startswith('W(') or n.startswith('$'),n
						
							considerupdating = [annJ] if updatelex and n.startswith('W(') else []
							for ann in considerupdating:
								if n in ann['nodes']: continue
								if n.startswith('W('):	# ensure single word is not already covered by a MW (CBBMW is OK)
									if any(lexnode.startswith('MW(') and n[2:-1] in mwtkns for lexnode,mwtkns in ann['node2words'].items()):
										continue
								elif n.startswith('CBBMW('):	# do not add a CBBMW if it overlaps with an MW
									cbbmwtkns = mergedJ['node2words'][n]
									if any(lexnode.startswith('MW(') and set(cbbmwtkns)&set(mwtkns) for lexnode,mwtkns in ann['node2words'].items()):
										continue
								ann['nodes'].append(n)
								if n in mergedJ['node2words']:
									ann['node2words'][n] = list(mergedJ['node2words'][n])
									
				
	
				if updatelex:
					yy = {k for k in mergedJ['node2words'] if k not in annJ['node2words'] and not k.startswith('CBBMW(')}
					assert not yy,(yy,mergedJ['nodes'],mergedJ['node2words'],annJ['nodes'],annJ['node2words'])
					xx = {k for k in annJ['node2words'] if k not in mergedJ['node2words']}
				else:
					xx = {k for k in annJ['node2words'] if k not in mergedJ['node2words'] and (not k.startswith('MW(') or 'CBB'+k not in mergedJ['node2words'])}
				assert not xx,xx

					
				# a token may be used by multiple CBBMWs, but for any other type of lexical node it must appear only once
				tokenreps = Counter([t for tkns in mergedJ['node2words'].values() for t in tkns])
				tokennodetypes = defaultdict(set)
				for n,tkns in mergedJ['node2words'].items():
					for t in tkns:
						tokennodetypes[t].add(n[:n.index('(')])
				for tkn,reps in tokenreps.items():
					if reps>1:
						assert 'MW' not in tokennodetypes[tkn],('Token used in multiple lexical expressions, at least one of which is a MW',tkn,tokennodetypes)

	assert len(set(mergedJ['nodes']))==len(mergedJ['nodes']),('Nodes are not unique in merge: '+' '.join(n for n in mergedJ['nodes'] if mergedJ['nodes'].count(n)>1))
	for i in range(len(annsJ)):
		assert len(set(annsJ[i]['nodes']))==len(annsJ[i]['nodes']),('Nodes are not unique in annsJ['+str(i)+']: '+' '.join(n for n in annsJ[i]['nodes'] if annsJ[i]['nodes'].count(n)>1))

	lexnodes = {n for n in mergedJ['nodes'] if 'W(' in n}	# excluding root
	assert set(mergedJ['node2words'].keys())==lexnodes,('Mismatch between nodes and node2words in merge',j,lexnodes^set(mergedJ['node2words'].keys()),mergedJ)
	
	# ensure single-word elements of CBBMWs also have their own entries
	for ann in [mergedJ]+(annsJ if updatelex else []):
		for n,tkns in ann['node2words'].items():
			if n.startswith('CBBMW('):
				for tkn in tkns:
					assert 'W('+tkn+')' in ann['node2words'],(tkn,ann['node2words'])
	
	# sort nodes by token order
	mergedJ['nodes'].sort(key=lambda n: ((['$$']+mergedJ['tokens']).index(mergedJ['node2words'][n][0]) if n in mergedJ['node2words'] else float('inf'),
										 n.split('(')[0]))
	
	return mergedJ


def main(annsFF, verbose=False, simplifycoords=False, updatelex=False, escapebrackets=False):
	assert len(annsFF)>=2
	
	i = 0
	allC = Counter()
	while True:	# iterate over items
		annsJ = []	# JSON input objects, one per annotator
		anns = []	# FUDG graphs, one per annotator
		locs = []
		
		try:
			for j,annsF in enumerate(annsFF):	# iterate over annotators
				#print('.',j,file=sys.stderr)
				ln = next(annsF)
				loc, sent, annJS = ln[:-1].split('\t')
				locs.append(loc)
				if j==0:
					sent0 = sent
				
				try:
					assert sent==sent0,(sent0,sent)	# TODO: hmm, why is this failing?
				except AssertionError as ex:
					print(ex, file=sys.stderr)

				
				annJ = json.loads(annJS)
				annsJ.append(annJ)
				if verbose:
					print(i, loc, '<<', sent, file=sys.stderr)
					print(annJ, file=sys.stderr)
				#a = FUDGGraph(annJ)
				#anns.append(a)
				
				if simplifycoords:
					aX = FUDGGraph(annJ)
					simplify_coord(aX)
					annsJ[-1] = annJ = aX.to_json_simplecoord()
					#if verbose: print(annJ, file=sys.stderr)
				
			mergedJ = merge(annsJ, updatelex=updatelex)
				
			output = '|'.join(locs) + '\t' + sent + '\t' + json.dumps(mergedJ)
		
			if verbose:
				print(output, file=sys.stderr)
				
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
		opts[{'-v': 'verbose', '-s': 'singleonly', '-c': 'simplifycoords', '-b': 'escapebrackets'}[args.pop(0)]] = True
	
	assert len(args)>=2
	
	while args:
		annsF = fileinput.input([args.pop(0)])
		annsFF.append(annsF)
	
	main(annsFF,**opts)
