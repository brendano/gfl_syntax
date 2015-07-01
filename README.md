Graph Fragment Language for Easy Syntactic Annotation
=====================================================

Software to support a lightweight dependency-style annotation language. The notation is called __GFL (Graph Fragment Language)__, and the formalism it expresses is called __FUDG (Fragmentary Unlabeled Dependency Grammar)__. These are introduced in

> [A Framework for (Under)specifying Dependency Syntax without Overloading Annotators](http://www.cs.cmu.edu/~nasmith/papers/schneider+oconnor+saphra+bamman+faruqui+smith+dyer+baldridge.law13.pdf)  
> Nathan Schneider, Brendan O’Connor, Naomi Saphra, David Bamman, Manaal Faruqui, Noah A. Smith, Chris Dyer, and Jason Baldridge.
> In _Proceedings of the 7th Linguistic Annotation Workshop & Interoperability with Discourse_, Sofia, Bulgaria, August 2013.

This repository contains supporting software developed by Nathan Schneider, Brendan O'Connor, Naomi Saphra, and Chris Dyer.

  - gflparser/ -- a parser for the GFL annotations format. It is implemented with a PEG (Parsing Expression Grammar).
    * parser/ contains code for a deprecated version of the annotation parser.
  - scripts/ -- a tool for checking GFL annotations (using the annotation parser), visualizing them in GraphViz, and converting them to other formats (including JSON).
  - [guidelines/guidelines.md]() -- annotation guidelines.
  - other directories contain some annotated sentences.
  - fudg_for_parsing.md -- describes conventions for converting GFL/FUDG graphs into conventional labeled dependency trees. 
  
For more information on GFL/FUDG, including a web annotation tool, see: http://www.ark.cs.cmu.edu/FUDG/

A FUDG dependency parser for tweets, and the data on which it was trained (Tweeboparser and Tweebank; Kong et al., EMNLP 2014) are available at: http://www.ark.cs.cmu.edu/TweetNLP/

Getting started
===============

The viewer needs Python 2.7 (including the [`parsimonious` library](https://pypi.python.org/pypi/parsimonious/)) and [GraphViz](http://www.graphviz.org/) (`dot` command) to be installed.  Run:

    scripts/view.py anno/tweets/dev.0000.anno
    scripts/view.py -w anno/tweets/dev.0000.anno
    scripts/view.py anno/nietzsche.anno

etc.

