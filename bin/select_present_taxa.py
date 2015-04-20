#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--tax', required=True)
parser.add_argument('-r', '--res', required=True)
parser.add_argument('-b', '--bp-cutoff', required=True, type=int)
parser.add_argument('-c', '--ctg-cutoff', required=True, type=int)
parser.add_argument('-p', '--present', required=True)

args = parser.parse_args()

# ----------------------------------------------------------------------------

out = open(args.present, 'w')

with open(args.tax) as f:
  line = f.readline()
  while not line.startswith(args.res):
    line = f.readline()
  
  line = f.readline()
  while not line == '\n':
    fields = line.split('\t')
    if int(fields[1]) >= args.ctg_cutoff and int(fields[3]) >= args.bp_cutoff:
      out.write('%s\t%s\n' % (fields[0], fields[3]))
    line = f.readline()

out.close()
