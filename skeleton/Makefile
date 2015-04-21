# NANOSCOPE PIPELINE: MASTER MAKEFILE
# This script starts the pipeline and executes the different steps one at a time
#
#------------------------------------------------------------------------------
#
# To start, use the nanoscope master script:
# 	nanoscope.py run <dir> -p <processors>
# Under the hood, the synchronization of the different steps of the pipeline
# are handled by GNU Make.
#
# To start the pipeline manually, one can also type:
# 	bash config-and-run.sh
# This will load the configuration and start the pipeline by invoking make.
# To reset the pipeline, one can type:
# 	make clean
#
# However, normal users will find it much more convenient to start/stop the 
# pipeline using the nanoscope.py tool.

#------------------------------------------------------------------------------
# Some default parameters:

ifeq '$(PROCESSORS)' ''
  export PROCESSORS:=4
endif

#------------------------------------------------------------------------------
# Commands:

all:
	make -C asm
	make -C classify
	make -C subspecies
	make -C abundance
	make -C results

asm.run:
	make -C asm

classify.run:
	make -C classify

subspecies.run:
	make -C subspecies

abundance.run: 
	make -C abundance

results.run:
	make -C results

clean:
	-rm *.done
	make -C asm clean
	make -C classify clean
	make -C subspecies clean
	make -C abundance clean
	make -C results clean
