FUDG JSON
=========

This document describes the JSON format for encoding FUDG annotation graphs. 
The GFL notation can be converted to JSON with the script `make_json.py`. 
The JSON format is recognized by the `FUDGGraph` data structure in `graph.py`, 
and is also the output format for `merge_annotations.py`.

FUDG JSON files
---------------

The file format consists of one sentence/annotated item per line, with three 
tab-separated columns:

  1. Annotation locator (e.g., the GFL annotation filename and offset)
  2. Raw input
  3. JSON object

An example line (wrapped for readability):

```json
ewtb55.anno.nschneid:52	Friendly , knowledgeable , and above all fair .	
	{"tokens": ["Friendly", ",", "knowledgeable", ",", "and", "above", "all", "fair", "."], 
	 "node_edges": [["$a", "W(Friendly)", "Conj"],
	 				["$a", "W(fair)", "Conj"],
	 				["$a", "W(knowledgeable)", "Conj"], 
	                ["W(fair)", "MW(above_all)", null]], 
	 "nodes": ["$a", "MW(above_all)", "W(Friendly)", "W(fair)", "W(knowledgeable)"], 
	 "extra_node2words": {"$a": [["and", "Coord"]]}, 
	 "node2words": {"W(fair)": ["fair"], 
	 				"W(knowledgeable)": ["knowledgeable"], 
	 				"MW(above_all)": ["all", "above"], 
	 				"W(Friendly)": ["Friendly"]}}
```

The contents of the JSON object are described below.

`"tokens"`
----------

All the tokens in the input. (Not including the root node.)

`"nodes"`
---------

The following types of nodes are allowed:

- dollar sign variables (e.g. for coordination nodes): `$a`
- the root node, if it participates in some edge in the annotation: `W($$)`
  * TODO: use `$$` instead?
- single words: `W(fair)`
- multiwords: `MW(above_all)`
- CBB multiwords, a compromise between annotations which do not agree on multiwords 
  (these are to be interpreted as CBBs in the graph): `CBBMW(above_all)`
- CBBs: `CBB1`

`"node2words"`
--------------

The root node (if present) and every single word, multiword, and CBB multiword should 
be mapped to a list of tokens that are subsumed by that node.

  * the root node is mapped to pseudo-token `"$$"` (TODO: get rid of this?)
  * tokens belonging to a multiword must not also appear in any other lexical node (another multiword or a single-word or CBBMW node)
  * single-word tokens and their subsumed CBBMWs should both have entries

`"extra_node2words"`
--------------------

This maps each coordination variable to a list of coordinator links. 
Each of these links contains the coordinator node and the label `"Coord"`.

`"node_edges"`
--------------

Includes:

- regular dependency links of type `null`
- CBB membership links of type `"cbbhead"` or `"unspec"`
- conjunct links of type `"Conj"`
- anaphoric links of type `"Anaph"`

Excludes:

- CBBMW membership links
- coordinator links

