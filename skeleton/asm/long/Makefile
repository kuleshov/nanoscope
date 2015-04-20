# LONG-READ ASSEMBLY USING CELERA
# If long reads are given, assembles them into contigs.
# Input files: LONG_READ_FASTQ
# Output file: long.fasta

#------------------------------------------------------------------------------
# High-level commands

all.done all:
	if [ -n "$(LONG_READ_FASTQ)" ]; then \
	make run && \
	ln -s ./run/9-terminator/long.ctg.fasta long.fasta; \
	else \
	make skip; \
	fi
	touch $@

skip:
	touch long.fasta
	touch all.done

clean:
	-rm -r celera.spec input.frg run long.fasta all.done

#------------------------------------------------------------------------------
# Assembler instructions

input.frg: $(LONG_READ_FASTQ)
	ln -s ../../config-files/celera.spec
	$(CELDIR)/fastqToCA \
	  -nonrandom \
	  -reads $< \
	  -libraryname 0 \
	  -technology none \
	  -feature forceBOGunitigger 0 \
	  -feature doNotTrustHomopolymerRuns 0 \
	  -feature discardReadsWithNs 0 \
	  -feature doNotQVTrim 0 \
	  -feature deletePerfectPrefixes 0 \
	  -feature doNotOverlapTrim 0 \
	  -feature isNotRandom 0 \
	  -feature fastqQualityValues sanger \
	  > $@

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
