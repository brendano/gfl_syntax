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

An example line:

    ewtb55.anno.nschneid:52	Friendly , knowledgeable , and above all fair .	{...JSON...}

The contents of the JSON object are described below.

`"tokens"`
----------

All the tokens in the input. (Not including the root node.)

`"nodes"`
---------

The following types of nodes are allowed:

- dollar sign variables (e.g. for coordination nodes): `$a`
- the root node, if it participates in some edge in the annotation: `**`
- single words: `W(fair)`
- multiwords: `MW(above_all)`
- FE multiwords, a compromise between annotations which do not agree on multiwords 
  (these are to be interpreted as FEs in the graph): `FEMW(above_all)`
- FEs: `FE1`

`"n2w"` (nodes-to-words)
------------------------

The root node (if present) and every single word, multiword, and FE multiword should 
be mapped to a list of tokens that are subsumed by that node.

  * tokens belonging to a multiword must not also appear in any other lexical node (another multiword or a single-word or FEMW node)
  * single-word tokens and their subsumed FEMWs should both have entries

`"varnodes"`
------------

This lists coordination variable nodes.

`"coords"`
----------

This is a list of coordinations. Each coordination is a 3-element list containing

- the coordination variable (which also appears in `"varnodes"`),
- a list of conjunct nodes, and
- a list of coordinator nodes

`"node_edges"`
--------------

Includes:

- regular dependency links of type `null`
- FE membership links of type `"fe*"` or `"fe"`
- conjunct links of type `"Conj"`
- coordinator links of type `"Coord"`
- anaphoric links of type `"Anaph"`

Excludes:

- FEMW membership links

`"anaph"`
---------

This contains anaphoric links only. Each link is a list of length 2.

`"deps"`
--------

This contains directed dependencies only—no `"Anaph"`, `"Coord"`, or `"Conj"` edges.


Example annotations and their JSON representation
-------------------------------------------------

> @X_SarahHumes_X @KamilaMerrygold Jesus are you two still at it ? Lolx

    Jesus**
    are** < (you two) 
    are** < [still at it]
    Lolx**

```json
{"tokens": ["@X_SarahHumes_X", "@KamilaMerrygold", "Jesus", "are", "you", "two", "still", "at", "it", "?", "Lolx"], 
	"n2w": {"W(are)": ["are"], 
			"W(two)": ["two"], 
			"W(Jesus)": ["Jesus"], 
			"MW(still_at_it)": ["still", "at", "it"], 
			"W(Lolx)": ["Lolx"], 
			"W(you)": ["you"]}, 
	"varnodes": [], 
	"deps": [["FE1", "W(you)", "fe"], ["**", "W(Lolx)", null], ["W(are)", "MW(still_at_it)", null], ["**", "W(Jesus)", null], ["FE1", "W(two)", "fe"], ["**", "W(are)", null], ["W(are)", "FE1", null]], 
	"anaph": [], 
	"coords": [], 
	"nodes": ["W(are)", "W(two)", "W(Jesus)", "MW(still_at_it)", "W(Lolx)", "W(you)", "FE1", "**"], 
	"node_edges": [["W(are)", "FE1", null], ["W(are)", "MW(still_at_it)", null], ["**", "W(Jesus)", null], ["FE1", "W(two)", "fe"], ["**", "W(Lolx)", null], ["FE1", "W(you)", "fe"], ["**", "W(are)", null]]}
```


> Friendly , knowledgeable , and above all fair .

    $a :: {Friendly knowledgeable fair} :: {and}
    [above all] > fair

```json
{"tokens": ["Friendly", ",", "knowledgeable", ",", "and", "above", "all", "fair", "."], 
	"n2w": {"W(fair)": ["fair"], "W(knowledgeable)": ["knowledgeable"], "MW(above_all)": ["all", "above"], "W(Friendly)": ["Friendly"], "W(and)": ["and"]},
	"varnodes": ["$a"],
	"deps": [["W(fair)", "MW(above_all)", null]],
	"anaph": [], 
	"coords": [["$a", ["W(fair)", "W(knowledgeable)", "W(Friendly)"], ["W(and)"]]], 
	"nodes": ["W(fair)", "W(knowledgeable)", "MW(above_all)", "W(Friendly)", "W(and)", "$a"],
	"node_edges": [["W(fair)", "MW(above_all)", null], ["$a", "W(knowledgeable)", "Conj"], ["$a", "W(Friendly)", "Conj"], ["$a", "W(fair)", "Conj"], ["$a", "W(and)", "Coord"]]}
```

> Cheap Hotel Rome - Thanks for all your help !

    [Cheap Hotel Rome]**
    Thanks** < for < ({all your} > help)
    your = [Cheap Hotel Rome]

```json
{"tokens": ["Cheap", "Hotel", "Rome", "-", "Thanks", "for", "all", "your", "help", "!"], 
	"n2w": {"W(your)": ["your"], "W(all)": ["all"], "W(Thanks)": ["Thanks"], "W(for)": ["for"], "W(help)": ["help"], "MW(Cheap_Hotel_Rome)": ["Rome", "Hotel", "Cheap"]}, 
	"varnodes": [], 
	"deps": [["W(help)", "W(your)", null], ["**", "MW(Cheap_Hotel_Rome)", null], ["W(help)", "W(all)", null], ["W(Thanks)", "W(for)", null], ["**", "W(Thanks)", null], ["W(for)", "W(help)", null]], 
	"anaph": [["W(your)", "MW(Cheap_Hotel_Rome)"]], 
	"coords": [], 
	"nodes": ["W(help)", "W(all)", "W(Thanks)", "W(for)", "W(your)", "MW(Cheap_Hotel_Rome)", "**"], 
	"node_edges": [["**", "W(Thanks)", null], ["W(help)", "W(all)", null], ["W(for)", "W(help)", null], ["W(your)", "MW(Cheap_Hotel_Rome)", "Anaph"], ["W(help)", "W(your)", null], ["W(Thanks)", "W(for)", null], ["**", "MW(Cheap_Hotel_Rome)", null]]}
```

Changes from pre-release version
--------------------------------

The following were changed from our preliminary implementation of the GFL/FUDG tools:

    CBBs ("Can't Be Bothered" expressions) renamed to FEs ("Fudge Expressions")
    dependency types: cbbhead -> fe*, unspec -> fe
    

    node2words -> n2w
    W($$) -> **; root no longer appears in n2w
    "extra_node2words": {"$a": [["and", "Coord"]]}
     -> "varnodes": ["$a"], "coords": [["$a", ["W(here's)", "W(saw)"], ["W(and)"]]]; "node_edges" now contains "Coord" as well as "Conj" edges; "nodes" and "n2w" now contain lexical nodes for coordinators

    new: anaph (anaphoric links)
    new: deps (directed dependencies only; no Anaph, Coord, or Conj edges)
