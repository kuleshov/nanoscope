#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pysam

ref = pysam.FastaFile('path/to/ref.fasta')

ctgs = dict()
for line in sys.stdin:
  fields = line.strip().split()
  
  ctg = fields[0]
  if ctg not in ctgs: ctgs[ctg] = set()
  fields[6] = fields[6].strip(',')
  for pa in fields[6].split(','):
    p, a = pa.split(':')
    p = int(p)
    ref_a = ref.fetch(ctg, p, p+1)
    if a != ref_a:
      ctgs[ctg].add(p)

for ctg, P in ctgs.iteritems():
  for p in P:
    print '%s\t%d\t%d' % (ctg, p, p)
