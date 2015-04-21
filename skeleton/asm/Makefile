# METAGENOMIC ASSEMBLY STAGE
# Input files:
#     SHORT_READ_PAIRED_FASTQ1, SHORT_READ_PAIRED_FASTQ2, SHORT_READ_UNPAIRED_FASTQ
#     LONG_READ_FASTQ, CONTIGS
# Output file: asm.fasta


#------------------------------------------------------------------------------
# General instructions

all:
	-rm contigs.fasta
	if [ "$(SKIP_ASM)" = "True" ]; then \
	  make skip; \
	elif [ "$(USE_SPADES)" = "True" ]; then \
	  make spades; \
	  ln -s ./spades/contigs.fasta; \
	else \
	  make -C short && \
	  make -C long && \
	  make -C joint && \
	  ln -s joint/joint.fasta contigs.fasta; \
	fi

skip:
	ln -s $(PRE_ASM_CONTIGS) contigs.fasta

clean:
	-rm all.done contigs.fasta
	-rm -r spades
	make -C short clean
	make -C long clean
	make -C joint clean

#------------------------------------------------------------------------------
# Assembly using SPAdes

ifneq '$(SHORT_READ_PAIRED_FASTQ1)' ''
  SPADES_INPUT:=-s $(LONG_READ_FASTQ) -1 $(SHORT_READ_PAIRED_FASTQ1) -2 $(SHORT_READ_PAIRED_FASTQ2)
endif
ifneq '$(SHORT_READ_UNPAIRED_FASTQ)' ''
  SPADES_INPUT:=--s1 $(LONG_READ_FASTQ) --s2 $(SHORT_READ_UNPAIRED_FASTQ)
endif
ifneq '$(PRE_ASM_CONTIGS)' ''
  SPADES_INPUT:=$(SPADES_INPUT) --trusted-contigs $(PRE_ASM_CONTIGS)
endif

spades:
	$(SPADES) \
	  -o ./spades \
	  -t $(PROCESSORS) \
	  $(SPADES_OPT) \
	  $(SPADES_INPUT)

