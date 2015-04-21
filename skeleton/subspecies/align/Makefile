# ALIGNMENT OF LONG READS TO ASSEMBLED CONTIGS
# Input files: REF and LONG_READ_FASTQ
# Output files: lr.sorted.bam lr.sorted.bam.bai

SHELL=/bin/bash -e -o pipefail

#------------------------------------------------------------------------------
# High-level commands

all:
	make lr.sorted.bam.bai

clean:
	-rm ref.* *.bam.*

#------------------------------------------------------------------------------
# Implementation

REF:=../../asm/contigs.fasta

ref.fasta: $(REF)
	-rm $@
	ln -s $< $@

ref.fasta.bwt: ref.fasta
	$(BWA) index $<

lr.sorted.bam: ref.fasta ref.fasta.bwt $(LONG_READ_FASTQ)
	$(BWA) mem -t $(PROCESSORS) $< $(LONG_READ_FASTQ) | $(SAMTOOLS) view -bS - | $(SAMTOOLS) sort - tmp.sorted
	mv tmp.sorted.bam $@

lr.sorted.bam.bai: lr.sorted.bam
	$(SAMTOOLS) index $<
