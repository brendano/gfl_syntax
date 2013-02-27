#!/usr/bin/env python2.7
"""
Convert treebank-style dependency parses to FUDG JSON data structures (one per line).

Arguments: <disambiguated_tokens_one_per_line> <dep_parses_pennconverter_tab_format>

@author: Manaal Faruqui (mfaruqui@cs.cmu.edu)
@since: 2013-02-18
"""
# Edges are like this: [to, from , None]

import sys, json

ROOT = "W($$)"

rawFile = sys.argv[1]
depFile = sys.argv[2]

def get_edges(nodeIndices, indexedEdges, puncNodes):
    
    node_edges = []
    for (fromNode, toNode) in indexedEdges:
      if fromNode in puncNodes and toNode in puncNodes:
         pass
      elif fromNode in puncNodes:
         pass
      elif toNode in puncNodes:
         node_edges.append([ROOT, nodeIndices[fromNode], None])
      else:
         if toNode == '0':
            node_edges.append([ROOT, nodeIndices[fromNode], None])
         else:
            node_edges.append([nodeIndices[toNode], nodeIndices[fromNode], None])

    return node_edges

def dump_data(tokens, nodes, puncNodes, nodeIndices, node2words, indexedEdges):
    
    node_edges = get_edges(nodeIndices, indexedEdges, puncNodes)
    sent_struct = {'tokens': tokens, 'nodes': nodes, 'node2words': node2words, 'node_edges': node_edges}
    #print 'tokens:', tokens
    #print 'nodes:', nodes
    #print 'punc nodes:', puncNodes
    #print 'node2words:', node2words
    #print 'node_edges:', node_edges
    print json.dumps(sent_struct)
    
def initialize():
    
    return ([],[ROOT],[],{},{},[])

tokens, nodes, puncNodes, nodeIndices, node2words, indexedEdges = initialize()

for lineRaw, lineDep in zip(open(rawFile,'r'),open(depFile, 'r')):
    
    lineDep = lineDep.strip()
    lineRaw = lineRaw.strip()
    
    if lineDep == '':
        dump_data(tokens, nodes, puncNodes, nodeIndices, node2words, indexedEdges)
        tokens, nodes, puncNodes, nodeIndices, node2words, indexedEdges = initialize()
        continue
    
    index, word, pos, info = lineDep.split('\t')
    connTo, role = info.split('/')

    word = lineRaw

    if pos not in ('.',',',':','(',')',"``","''","`","'",'"'):
        node = 'W('+word+')'
        tokens.append(word)
        nodes.append(node)
        nodeIndices[index] = node
        node2words[node] = word
        indexedEdges.append((index, connTo))
    else:
        #node = 'W('+word+')'
        tokens.append(word)
        #nodes.append(node)
        puncNodes.append(index)
        #nodeIndices[index] = node
        #node2words[node] = word
        indexedEdges.append((index, connTo))

dump_data(tokens, nodes, puncNodes, nodeIndices, node2words, indexedEdges)
