import os,sys,re,cgi
from collections import defaultdict

# 28849570224             @ciaranyree it was on football wives , one of the players and his wife own smash burger @ O V P N N , $ P D N & D N V ^ ^       kgimpel@ANDREW.CMU.EDU  Thu Feb 17 2011 13:29:43 GMT-0500 (Eastern Standard Time)

outbase = sys.argv[1]

for tweet_i,line in enumerate(sys.stdin):
  parts = line.split('\t')
  tweet_id = parts[0]
  tokens = parts[2].split()
  poses = parts[3].split()

  seen_words = set()
  words_needing_dedup = set()

  counts = defaultdict(int)
  for tok in tokens: counts[tok] += 1
  words_needing_dedup = {w for w in counts if counts[w] > 1}

  def needs_dedup(i):
    if tokens[i] not in words_needing_dedup: return False
    p = poses[i]
    if p==',': return False
    if p=='!': return False
    return True

  output_tokens = []
  counters = defaultdict(lambda:0)
  for i,(tok,pos) in enumerate(zip(tokens,poses)):
    if needs_dedup(i):
      counters[tok] += 1
      tok = tok + '^' + str(counters[tok])
    output_tokens.append(tok)

  with open("%s.%04d.anno" % (outbase, tweet_i),'w') as f:
    print>>f, "---"
    print>>f, "% ID", tweet_id
    print>>f, "% POS TEXT"
    print>>f, ' '.join('%s/%s' % (tok,pos) for tok,pos in zip(tokens,poses)) 
    print>>f, "% TARGET TEXT"
    print>>f, ""
    print>>f, ' '.join(output_tokens)
    print>>f, ""
    print>>f, "% ANNO"
    print>>f, ""
    print>>f, ' '.join(output_tokens)


