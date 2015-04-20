#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

out_line = ""
name_line = ""
line = sys.stdin.readline()
while line:
  line = line.strip()
  if line.startswith('>') or line.startswith('@'):
    if out_line:
      print name_line
      print out_line
    out_line = ""
    name_line = line
  elif line.isalpha():
    out_line += line
  else:
    raise ValueError("Invalid characters found in FASTA file")

  line = sys.stdin.readline()

if out_line:
  print name_line
  print out_line
