FUDG representation for parsing
===============================

Nathan Schneider & Lingpeng Kong  
2013-10-25

Apart from underspecification and coreference, which we will not be predicting in the output of our parser, the FUDG formalism differs from traditional dependency parsing in a few respects:

1. Special demarcation of **utterances** within the input
2. Ability to **exclude** some input tokens from the parse
3. Ability to group tokens into **multiword** lexical nodes
4. Special representation of **coordinate** structures

All of these are specified in a GFL annotation. We propose to treat (1) and (2) as **preprocessing** steps at test time, so the TurboParser model assumes it sees one utterance at a time and knows which tokens are relevant.

(3) and (4) can be treated by **transforming** the FUDG graph into a traditional dependency tree with special edges. This process is deterministic and bidirectional, so at test time the TurboParser prediction can be converted to the FUDG-style graph. An example illustrating the transformations:

> I want fresh bread and~1 butter and~2 jam as~1 well as~2 tea.

GFL:

    I > want < $awa
    $awa :: {$aa tea} :: {[as well as]}
    $aa :: {bread butter jam} :: {and~1 and~2}
    fresh > $aa
    
Transformed FUDG:

    I > want < as~1
    
    well -MWE> as~1 <MWE- as~2
    
    and~1 -CONJ> as~1
    tea -CONJ> as~1
    
    and~1 <COORD- and~2
    
    bread -CONJ> and~1
    butter -CONJ> and~1
    jam -CONJ> and~1
    fresh > and~1

Note that:

  - MWEs are encoded as the first token heading the other tokens. Constraints: MWE edges are sensitive to original token order (the head must appear earlier); MWE edge dependents are not allowed to have their own dependents.
  - Coordinators serve as heads of the coordinated phrase, removing the need for special coordinator nodes. The conjuncts attach with CONJ edges; modifiers attach with unlabeled edges. If there are multiple coordinators, the first one heads them all with COORD edges (and nothing is allowed to attach to these other coordinators).