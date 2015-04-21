#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import shutil

STAGES = ['asm', 'classify', 'subspecies', 'abundance', 'results']
NS_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# ----------------------------------------------------------------------------

def main():
  parser = argparse.ArgumentParser(description="")
  subparsers = parser.add_subparsers(title='Commands')

  # Init

  init_parser = subparsers.add_parser('init', help='Initialize pipeline')
  init_parser.set_defaults(func=init)

  init_parser.add_argument('folder', help='Pipeline folder', action=NewFolder)
  init_parser.add_argument('-l', '--long', help='Long reads fastq',  required=True, action=ValidPath)
  init_parser.add_argument('-s', '--short-single', help='Short reads fastq (unpaired)', required=False, default="", action=ValidPath)
  init_parser.add_argument('-p', '--short-paired', help='Short reads fastq (paired)', required=False, default="", action=ValidPathList, nargs=2)
  init_parser.add_argument('-c', '--contigs', help='Pre-assembled contigs', nargs='+', required=False, default="", action=ValidPathList)
  init_parser.add_argument('--short-insert-size', help='Short read insert size', default=500, type=int, required=False)
  init_parser.add_argument('--short-read-length', help='Short read insert size', default=101, type=int, required=False)
  init_parser.add_argument('--path', help='Path to nanoscope', default=NS_PATH, required=False, action=ValidPath)

  # Run

  run_parser = subparsers.add_parser('run', help='Start/resume pipeline')
  run_parser.set_defaults(func=run)

  run_parser.add_argument('folder', help='Pipeline folder', action=ValidPath)
  run_parser.add_argument('-p', '--processors', help='Number of processors to use', type=int, default=4)
  run_parser.add_argument('-r', '--restart', help='Resume pipeline from the begginning', action='store_true', required=False)
  run_parser.add_argument('--up-to', help='Compute up to given stage', default=STAGES[-1])
  run_parser.add_argument('--skip-asm', help='Skip read assembly', action='store_true')
  run_parser.add_argument('--skip-minimus', help='Skip minimus contig merging', action='store_true')
  run_parser.add_argument('--spades', help='Assemble short and long reads with spades', action='store_true')

  # Parse args
  args = parser.parse_args()
  args.func(args)

# ----------------------------------------------------------------------------
# Command handlers

def init(args):
  args = _handle_args(args)

  # copy the skeleton to destination folder
  SK_PATH = args.path + '/skeleton/'
  try:
    shutil.copytree(SK_PATH, args.folder)
  except ValueError:
    exit("Could not initialize pipeline")

  # set parameters
  try:
    f = open(SK_PATH + '/config-and-run.sh')
  except ValueError:
    exit("Could not open config file in %s" % SK_PATH)
  else:
    with f:
      content = f.read()
      if args.short_paired:
        short_paired1 = args.short_paired[0]
        short_paired2 = args.short_paired[1]
      else:
        short_paired1, short_paired2 = "", ""
      content = content.format(
          short_paired1=short_paired1,
          short_paired2=short_paired2,
          short_unpaired=args.short_single,
          long=args.long, contigs=' '.join(args.contigs),
          short_insert_size=args.short_insert_size,
          short_read_length=args.short_read_length,
          nanoscope_path=args.path
        )
      try:
        g = open(args.folder + '/config-and-run.sh', 'w')
      except ValueError:
        with g:
          exit('Could not write config to %s' % SK_PATH)
      else:
        g.write(content)

def run(args):
  cmd = "cd %s; " % args.folder
  if args.restart:
    cmd += "make clean; "
  target_stage_names = STAGES[:STAGES.index(args.up_to)+1]
  target_stages = ' '.join([stage + '.run' for stage in target_stage_names])
  cmd += "bash config-and-run.sh %s PROCESSORS=%d" % (target_stages, args.processors)
  if args.skip_asm:
    cmd += ' SKIP_ASM="True"'
  if args.skip_minimus:
    cmd += ' SKIP_MINIMUS="True"'
  if args.spades:
    cmd += ' USE_SPADES="True"'
  print cmd

  # subprocess.Popen(cmd, shell=True, executable='/bin/bash')
  return_code = subprocess.call(cmd, shell=True)
  if return_code != 0:
    exit("Pipeline execution failed in %s" % args.folder)

# ----------------------------------------------------------------------------
# Helpers

class NewFolder(argparse.Action):
  def __call__(self,parser, namespace, arg, option_string=None):
    arg = os.path.abspath(arg)
    if not arg:
      parser.error("Pipeline folder not specified")
    elif os.path.exists(arg):
      parser.error("%s already exists; please specify a new folder" % arg)
    else:
      setattr(namespace,self.dest,arg)

class ValidPath(argparse.Action):
  def __call__(self,parser, namespace, arg, option_string=None):
    arg = os.path.abspath(arg)
    if not arg:
      parser.error("Pipeline folder not specified")
    elif not os.path.exists(arg):
      parser.error("%s does not exist" % arg)
    else:
      setattr(namespace,self.dest,arg)

class ValidPathList(argparse.Action):
  def __call__(self,parser, namespace, args, option_string=None):
    parsed_args = list()
    for arg in args:
      arg = os.path.abspath(arg)
      if not arg:
        parser.error("Pipeline folder not specified")
      elif not os.path.exists(arg):
        parser.error("%s does not exist" % arg)
      else:
        parsed_args.append(arg)
    setattr(namespace,self.dest,parsed_args)

def _handle_args(args):
  if not (args.short_paired or args.short_single):
    print "Warning: Abundance estimation must be skipped as there are no short read libraries"
  # if not (args.skip_asm and not args.contigs):
  #   print "Error: Must provide pre-assembled contigs if assembly is to be skipped"

  return args


if __name__ == '__main__':
  main()
