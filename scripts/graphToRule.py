#!/usr/bin/env python2.7

"""
Convert a gfl graph to a set of human readable dependency rules.

@author: Manaal Faruqui (mfaruqui@cs.cmu.edu)
@since: 2013-04-26
"""

"""
TODOs

1. Sort tokens by their indices in CBBs
2. Handle coordination nodes
3. Check validity on more number of graphs
"""

from copy import deepcopy
from graph import *

def print_list(listNodes):
    
    if len(listNodes) == 1:
        return
    
    print listNodes[0],
    for nodeName in listNodes[1:]:
        print "<", nodeName,
    print 
    
def print_reverse_list(listNodes):
    
    if len(listNodes) == 1:
        return
        
    print listNodes[-1],
    # do not print the head
    for i in range(len(listNodes)-2, 0, -1):
        print ">", listNodes[i],
    print ">", 

#Merge two rules if their heads are identical
def merge_and_print_rules(listPaths):
    
    i = 0
    while i < len(listPaths)-1:
        path1 = listPaths[i]
        path2 = listPaths[i+1]
        
        if path1[0] == path2[0]:
            print_reverse_list(path1)
            print_list(path2)
            i += 2
        else:
            print_list(path1)
            i += 1
            
    if i == len(listPaths)-1:
        print_list(listPaths[i])

#Collecting all the CBB members to be printed together
def collect_cbb_members(node):
    
    cbbName = '( '
    for member in node.members:
        if member.isCBB:
            cbbName += collect_cbb_members(member)
        else:
            cbbName += member.name
        cbbName += ' '
    cbbName += ')'
    
    return cbbName

#Recursively traverse the graph while storing the
#rules in listPaths[]
def traverse(node, path, listPaths):
    
    if node.isCBB:
        path.append(collect_cbb_members(node))
        listPaths.append(path)
        for childNode in node.members:
            traverse(childNode, [], listPaths)
        return
    else:
        path.append(node.name)
        
    if len(node.childedges) == 0:
        listPaths.append(path)
    elif len(node.childedges) > 1:
        listPaths.append(path)
        for (childNode, edgeLabel) in node.childedges:
            traverse(childNode, [node.name], listPaths)
    else:
        for (childNode, edgeLabel) in node.childedges:
            traverse(childNode, deepcopy(path), listPaths)
            
def get_dependency_rules(graph):
    
    listPaths = []
    traverse(graph.root, [], listPaths)
    listPaths.sort()
    
    newPaths = [path for path in listPaths if len(path) > 1]
    del listPaths
    
    return newPaths
        
if __name__=='__main__':
    g = {"tokens": ["I~1", "wish", "I~2", "had", "you~1", "as", "my~1", "dentist~1", "early", "on", "in", "my~2", "life", "-", "maybe", "my~3", "teeth", "would", "have", "been", "a", "lot", "better", "then", "they", "are~1", "now~1", ",", "However", "I~3", "am", "glad", "you~2", "are~2", "my~4", "dentist~2", "now~2", "."], "node_edges": [["CBB1", "CBB2", "unspec"], ["CBB1", "W(as)", "unspec"], ["CBB1", "W(had)", "unspec"], ["CBB2", "W(early)", "cbbhead"], ["CBB2", "W(in)", "unspec"], ["CBB2", "W(life)", "unspec"], ["CBB2", "W(my~2)", "unspec"], ["CBB2", "W(on)", "unspec"], ["W($$)", "W(However)", None], ["W($$)", "W(am)", None], ["W($$)", "W(wish)", None], ["W($$)", "W(would)", None], ["W(am)", "W(glad)", None], ["W(are~1)", "W(been)", "Anaph"], ["W(are~1)", "W(now~1)", None], ["W(are~1)", "W(they)", None], ["W(as)", "W(my~1)", None], ["W(been)", "W(better)", None], ["W(better)", "MW(a_lot)", None], ["W(better)", "W(then)", None], ["W(glad)", "W(are~2)", None], ["W(had)", "W(I~2)", None], ["W(had)", "W(you~1)", None], ["W(have)", "W(been)", None], ["W(my~1)", "W(dentist~1)", None], ["W(teeth)", "W(my~3)", None], ["W(then)", "W(are~1)", None], ["W(wish)", "CBB1", None], ["W(would)", "W(have)", None], ["W(would)", "W(maybe)", None], ["W(would)", "W(teeth)", None]], "nodes": ["CBB1", "CBB2", "MW(a_lot)", "W($$)", "W(However)", "W(I~2)", "W(am)", "W(are~1)", "W(are~2)", "W(as)", "W(been)", "W(better)", "W(dentist~1)", "W(early)", "W(glad)", "W(had)", "W(have)", "W(in)", "W(life)", "W(maybe)", "W(my~1)", "W(my~2)", "W(my~3)", "W(now~1)", "W(on)", "W(teeth)", "W(then)", "W(they)", "W(wish)", "W(would)", "W(you~1)"], "extra_node2words": {}, "node2words": {"W(I~2)": ["I~2"], "W(However)": ["However"], "W(would)": ["would"], "W(then)": ["then"], "W(maybe)": ["maybe"], "W(my~2)": ["my~2"], "W(life)": ["life"], "W(are~1)": ["are~1"], "W(on)": ["on"], "W(as)": ["as"], "W(have)": ["have"], "W(my~3)": ["my~3"], "W(my~1)": ["my~1"], "W(they)": ["they"], "W(in)": ["in"], "W($$)": ["$$"], "W(wish)": ["wish"], "W(had)": ["had"], "W(you~1)": ["you~1"], "W(teeth)": ["teeth"], "W(are~2)": ["are~2"], "W(now~1)": ["now~1"], "W(better)": ["better"], "W(dentist~1)": ["dentist~1"], "MW(a_lot)": ["a", "lot"], "W(glad)": ["glad"], "W(am)": ["am"], "W(been)": ["been"], "W(early)": ["early"]}}
    #g = {"tokens": ["I~1", "have~1", "purchased", "over", "15", "vehicles", "(", "cars", ",", "rvs", ",", "and~1", "boats", ")", "in", "my", "lifetime", "and~2", "I~2", "have~2", "to", "say", "the~1", "experience", "with", "Michael", "and~3", "Barrett", "Motor", "Cars", "of~1", "San", "Antonio", "was", "one", "of~2", "the~2", "best", "."], "node_edges": [["CBB1", "W(15)", "unspec"], ["CBB1", "W(I~1)", "unspec"], ["CBB1", "W(and~1)", "unspec"], ["CBB1", "W(boats)", "unspec"], ["CBB1", "W(cars)", "unspec"], ["CBB1", "W(have~1)", "cbbhead"], ["CBB1", "W(in)", "unspec"], ["CBB1", "W(lifetime)", "unspec"], ["CBB1", "W(my)", "unspec"], ["CBB1", "W(over)", "unspec"], ["CBB1", "W(purchased)", "unspec"], ["CBB1", "W(rvs)", "unspec"], ["CBB1", "W(vehicles)", "unspec"], ["CBB2", "W(Antonio)", "unspec"], ["CBB2", "W(Barrett)", "unspec"], ["CBB2", "W(Cars)", "unspec"], ["CBB2", "W(Michael)", "unspec"], ["CBB2", "W(Motor)", "unspec"], ["CBB2", "W(San)", "unspec"], ["CBB2", "W(and~3)", "unspec"], ["CBB2", "W(experience)", "unspec"], ["CBB2", "W(of~1)", "unspec"], ["CBB2", "W(the~1)", "unspec"], ["CBB2", "W(with)", "unspec"], ["CBB3", "W(best)", "unspec"], ["CBB3", "W(of~2)", "unspec"], ["CBB3", "W(one)", "unspec"], ["CBB3", "W(the~2)", "unspec"], ["MW(have~2_to)", "W(I~2)", None], ["MW(have~2_to)", "W(say)", None], ["W($$)", "CBB1", None], ["W($$)", "MW(have~2_to)", None], ["W($$)", "W(and~2)", None], ["W(say)", "W(was)", None], ["W(was)", "CBB2", None], ["W(was)", "CBB3", None]], "nodes": ["CBB1", "CBB2", "CBB3", "MW(have~2_to)", "W($$)", "W(15)", "W(Antonio)", "W(Barrett)", "W(Cars)", "W(I~1)", "W(I~2)", "W(Michael)", "W(Motor)", "W(San)", "W(and~1)", "W(and~2)", "W(and~3)", "W(best)", "W(boats)", "W(cars)", "W(experience)", "W(have~1)", "W(in)", "W(lifetime)", "W(my)", "W(of~1)", "W(of~2)", "W(one)", "W(over)", "W(purchased)", "W(rvs)", "W(say)", "W(the~1)", "W(the~2)", "W(vehicles)", "W(was)", "W(with)"], "extra_node2words": {}, "node2words": {"W(San)": ["San"], "W(I~2)": ["I~2"], "W(and~2)": ["and~2"], "W(the~2)": ["the~2"], "W(lifetime)": ["lifetime"], "W(say)": ["say"], "W(Barrett)": ["Barrett"], "W(purchased)": ["purchased"], "W(vehicles)": ["vehicles"], "W(15)": ["15"], "W(Cars)": ["Cars"], "W(experience)": ["experience"], "W(with)": ["with"], "W(over)": ["over"], "W(rvs)": ["rvs"], "W(my)": ["my"], "W(cars)": ["cars"], "W(in)": ["in"], "W(boats)": ["boats"], "W(I~1)": ["I~1"], "W(and~3)": ["and~3"], "W($$)": ["$$"], "W(the~1)": ["the~1"], "W(was)": ["was"], "W(and~1)": ["and~1"], "W(Motor)": ["Motor"], "W(of~1)": ["of~1"], "W(one)": ["one"], "W(have~1)": ["have~1"], "W(Antonio)": ["Antonio"], "MW(have~2_to)": ["to", "have~2"], "W(of~2)": ["of~2"], "W(best)": ["best"], "W(Michael)": ["Michael"]}}
    graph = FUDGGraph(g)
 
    rules = get_dependency_rules(graph)
    merge_and_print_rules(rules)