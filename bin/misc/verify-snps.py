#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pysam

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--bam', required=True)
parser.add_argument('-c', '--clusters', required=True)
parser.add_argument('-s', '--bad-snps', required=True)
parser.add_argument('--support', default=2, type=int)

args = parser.parse_args()

# ----------------------------------------------------------------------------

clusters = dict()
types = dict()
n_tot_pos = 0
n_var_pos = 0
with open(args.clusters) as f:
  for line in f:
    fields = line.strip().split()
    if len(fields) == 1: continue
    positions, alleles, vartypes = zip(*[fi.split(':') for fi in fields[1].split(',')])
    clusters[fields[0]] = dict((int(p), a) for p, a in zip(positions, alleles)) 
    types[fields[0]] = dict((int(p), t) for p, t in zip(positions, vartypes)) 
    n_tot_pos += len(positions)
    n_var_pos += len([t for t in vartypes if t == 'V'])

print '%d positions loaded.' % n_tot_pos
print '%d variant positions loaded.' % n_var_pos


bam = pysam.Samfile(args.bam)
bad = open(args.bad_snps, 'w')
ref_lengths = dict(zip(bam.references, bam.lengths))

n_confirmed_positions = 0
n_tested_positions = 0
n_confirmed_var_positions = 0
n_tested_var_positions = 0
for cluster, positions in sorted(clusters.iteritems()):
  for pos, allele in sorted(positions.iteritems()):
    if allele == '-' or allele.startswith('I'):
      continue
    # print
    if n_tested_positions % 1000 == 0:
      print n_tested_positions, n_tot_pos, '|', n_confirmed_positions, n_tested_positions, '|', n_confirmed_var_positions, n_tested_var_positions
    pileup = bam.pileup(reference=cluster, start=pos, end=pos+1, truncate=True)
    num_confirming = 0
    for pcol in pileup:
      for pread in pcol.pileups:
        if pread.indel != 0: continue
        if pread.is_del: continue
        if pread.alignment.query_qualities[pread.query_position] < 20: continue
        seq = pread.alignment.query_sequence[pread.query_position]
        if seq == allele:
          num_confirming += 1
    if num_confirming >= 2:
      n_confirmed_positions += 1
      if types[cluster][pos] == 'V':
        n_confirmed_var_positions += 1
    else:
      bad.write('%s\t%d\n' % (cluster, pos))
    n_tested_positions += 1
    if types[cluster][pos] == 'V':
      n_tested_var_positions += 1

print n_confirmed_positions, n_tested_positions
print n_confirmed_var_positions, n_tested_var_positions

