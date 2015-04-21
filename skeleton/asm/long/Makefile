# LONG-READ ASSEMBLY USING CELERA
# If long reads are given, assembles them into contigs.
# Input files: LONG_READ_FASTQ
# Output file: long.fasta

#------------------------------------------------------------------------------
# High-level commands

all:
	if [ -n "$(LONG_READ_FASTQ)" ]; then \
	make run long.fasta; \
	else \
	make skip; \
	fi

skip:
	[ -e long.fasta ] || touch long.fasta

clean:
	-rm -r celera.spec input.frg run long.fasta 

#------------------------------------------------------------------------------
# Assembler instructions

input.frg: $(LONG_READ_FASTQ)
	ln -s ../../config-files/celera.spec
	$(CELDIR)/fastqToCA \
	  -reads $< \
	  -libraryname 0 \
	  $(CEL_LIB_FLAGS) > $@

run: input.frg
	-rm -r $@.tmp
	$(CELDIR)/runCA \
	  -d $@.tmp \
	  -p long \
	  -s celera.spec \
	  ovlCorrConcurrency=$(PROCESSORS) \
	  ovlConcurrency=$(PROCESSORS) \
	  frgCorrConcurrency=$(PROCESSORS) \
	  cnsConcurrency=$(PROCESSORS) \
	  $< > asm.out 2>&1
	mv $@.tmp $@

long.fasta: run/9-terminator/long.ctg.fasta
	ln -s $< $@
