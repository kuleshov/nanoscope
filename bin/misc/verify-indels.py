#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pysam

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--bam', required=True)
# parser.add_argument('-f', '--ref-fasta', required=True)
parser.add_argument('-c', '--clusters', required=True)
parser.add_argument('-s', '--bad-snps', required=True)
# parser.add_argument('-r', '--strange-reads', required=True)

args = parser.parse_args()

# ----------------------------------------------------------------------------

# load interesting positions
clusters = dict()
n_tot_pos = 0
with open(args.clusters) as f:
  for line in f:
    fields = line.strip().split()
    if len(fields) == 1: continue
    positions, alleles, postypes = zip(*[fi.split(':') for fi in fields[1].split(',')])
    clusters[fields[0]] = dict((int(p), a) for p, a in zip(positions, alleles)) 
    n_tot_pos += len(positions)

print '%d positions loaded.' % n_tot_pos

bam = pysam.Samfile(args.bam)
bad = open(args.bad_snps, 'w')
ref_lengths = dict(zip(bam.references, bam.lengths))

# now we finally look at the coverage
n_confirmed_positions = 0
n_tested_positions = 0
for cluster, positions in clusters.iteritems():
  for pos, allele in positions.iteritems():
    if n_tested_positions % 500 == 0:
      print n_tested_positions, n_tot_pos, '|', n_confirmed_positions, n_tested_positions
    if cluster not in bam.references: continue
    reads = bam.fetch(reference=cluster, start=pos, end=pos+1)
    num_confirming = 0
    num_total = 0
    for read in reads:
      align_positions = \
          [(align_read_p, align_ref_p) for (align_read_p, align_ref_p) in read.get_aligned_pairs()
           if align_ref_p == pos]
      if allele == '-':
        align_positions_prev = \
          [(align_read_p, align_ref_p) for (align_read_p, align_ref_p) in read.get_aligned_pairs()
           if align_ref_p == pos-1]
        if align_positions and align_positions_prev \
        and align_positions[0][1] and align_positions_prev[0][1] \
        and align_positions[0][1]-1 == align_positions_prev[0][1]:
          num_confirming += 1
      elif allele.startswith('I'):
        indel_len = len(allele[1:])
        read_p = align_positions[0][0]
        if align_positions[0][0]:
          if indel_len <= len(read.query_sequence[read_p:]):
            if ''.join(read.query_sequence[read_p:read_p+indel_len]) == allele[1:]:
              num_confirming += 1
      else:
        if not align_positions[0][0]: continue
        read_p = align_positions[0][0]
        if read.query_qualities and read.query_qualities[read_p] >= 20 \
        and read.query_sequence and read.query_sequence[read_p] == allele:
          num_confirming += 1
    if num_confirming >= 2:
      n_confirmed_positions += 1
    else:
      bad.write('%s\t%d\n' % (cluster, pos))
    n_tested_positions += 1

print n_confirmed_positions, n_tested_positions
