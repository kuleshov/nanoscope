#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pysam

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--haplotypes', required=True)
parser.add_argument('-r', '--ref', required=True)
parser.add_argument('-a', '--alleles', required=True)
parser.add_argument('-v', '--var-alleles', required=True)
parser.add_argument('-f', '--pos-field', type=int, default=4)
parser.add_argument('--snps-only', action='store_true')

args = parser.parse_args()

ref = pysam.FastaFile(args.ref)

haplotypes = dict()
haplotypes_all = dict()
n=0
with open(args.haplotypes) as haps:
  for line in haps:
    fields = line.strip().split()

    ctg = fields[0]
    haplotypes[n] = set()
    haplotypes_all[n] = set()
    f = args.pos_field
    fields[f] = fields[f].strip(',')
    for pa in fields[f].split(','):
      p, a = pa.split(':')
      if args.snps_only and (a == '-' or a.startswith('I')):
        continue
      p = int(p)
      ref_a = ref.fetch(ctg, p, p+1)
      if a != ref_a:
        haplotypes[n].add((ctg,p))
      haplotypes_all[n].add((ctg,p))
    n += 1

with open(args.alleles, 'w') as out:
  for h, P in haplotypes_all.iteritems():
    for ctg, p in P:
      out.write('%s\t%d\t%d\t%d\n' % (ctg, p, p, h))

with open(args.var_alleles, 'w') as out:
  for h, P in haplotypes.iteritems():
    for ctg, p in P:
      out.write('%s\t%d\t%d\t%d\n' % (ctg, p, p, h))
