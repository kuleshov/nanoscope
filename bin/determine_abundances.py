#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--taxa', required=True)
parser.add_argument('-c', '--ctgs', required=True)
parser.add_argument('-v', '--cov', required=True)
parser.add_argument('-r', '--res', required=True)
parser.add_argument('-l', '--read-len', required=True, type=int)
parser.add_argument('-a', '--abundances', required=True)
parser.add_argument('--median', action='store_true',
                    help='use the median contig coverage to determine'
                    'the abundance of a taxon (may work better at species level)')

args = parser.parse_args()

# ----------------------------------------------------------------------------

if args.res == 'STRAIN':
  res = 7
elif args.res == 'SPECIES':
  res = 6
elif args.res == 'GENUS':
  res = 5
elif args.res == 'FAMILY':
  res = 4
elif args.res == 'ORDER':
  res = 3
elif args.res == 'CLASS':
  res = 2
elif args.res == 'PHYLUM':
  res = 1
elif args.res == 'DOMAIN':
  res = 0
else:
  exit("Error: Invalid taxonomic resolution")

def median(L):
  sorted_L = sorted(L)
  n = len(sorted_L)

  if n % 2 == 1:
    return sorted_L[n/2]
  else:
    return (sorted_L[n/2-1] + sorted_L[n/2]) / 2.0

# ----------------------------------------------------------------------------

# get the taxonomic units:

taxa = set()
lr_coverages = dict()
with open(args.taxa) as f:
  for line in f:
    fields = line.strip().split()
    taxa.add(fields[0])
    lr_coverages[fields[0]] = int(fields[1])

# get the names of contigs associated with each taxonomic unit:

ctgs = dict()
with open(args.ctgs) as f:
  f.readline()
  for line in f:
    ctg, classification = line.split('\t')
    classes = classification.split(';')
    if classes[res] in taxa:
      if classes[res] not in ctgs: ctgs[classes[res]] = set()
      ctgs[classes[res]].add(ctg)

# get length of each contig and number of reads that map to it:

reads_mapped = dict()
lengths = dict()
with open(args.cov) as f:
  for line in f:
    fields = line.split()
    reads_mapped[fields[0]] = float(fields[2])
    lengths[fields[0]] = float(fields[1])


taxa_coverages = dict()
if args.median:
  # compute median coverage for each taxonomic unit:
  for tax in taxa:
    if tax not in ctgs: 
      continue
    coverages = [reads_mapped[ctg] * args.read_len / lengths[ctg]
                 for ctg in ctgs[tax] if ctg in reads_mapped 
                 and (lengths[ctg] > 10000 and reads_mapped[ctg] > 0) or lengths[ctg] > 20000]
    sizes = [lengths[ctg]
                 for ctg in ctgs[tax] if ctg in reads_mapped 
                 and ((lengths[ctg] > 10000 and reads_mapped[ctg] > 0) or lengths[ctg] > 20000)]
    reads_mapped_counts = [reads_mapped[ctg]
                 for ctg in ctgs[tax] if ctg in reads_mapped 
                 and ((lengths[ctg] > 10000 and reads_mapped[ctg] > 0) or lengths[ctg] > 20000)]
    if coverages:
      taxa_coverages[tax] = median(coverages)
    else:
      taxa_coverages[tax] = 0.0
else:
  for tax in taxa:
    if tax not in ctgs:
      continue
    coverages = [reads_mapped[ctg] * args.read_len / lengths[ctg]
                 for ctg in ctgs[tax] if ctg in reads_mapped]
    if coverages:
      taxa_coverages[tax] = median(coverages)
    else:
      taxa_coverages[tax] = 0.0

# print: taxon, short read coverage, long read coverage
out = open(args.abundances, 'w')
norm_factor = float(sum(taxa_coverages.values()))
out.write('#TAXON\tSHORT READ BP\tLONG READ BP\n')
for tax in taxa_coverages:
    out.write('%s\t%d\t%d\n' % (tax, taxa_coverages[tax], lr_coverages[tax]))
    #out.write('%s\t%f\n' % (tax, taxa_coverages[tax]))

out.close()

