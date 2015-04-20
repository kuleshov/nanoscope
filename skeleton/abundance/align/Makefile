# ALIGNMENT OF SHORT READS TO ASSEMBLED CONTIGS
# Input files:
# 	../../asm/contigs.fasta, SHORT_READ_PAIRED_FASTQ1,
# 	SHORT_READ_PAIRED_FASTQ2, SHORT_READ_UNPAIRED_FASTQ
# Output files: sr.sorted.bam sr.sorted.bam.bai

#------------------------------------------------------------------------------
# High-level commands

all.done all:
	make sr.sorted.q30.bam.bai
	touch $@

clean:
	-rm all.done rm ref.* *.bam.*

#------------------------------------------------------------------------------
# Implementation

REF:=../../asm/contigs.fasta

ref.fasta: $(REF)
	ln -s $< $@

ref.fasta.bwt: ref.fasta
	$(BWA) index $<

sr.sorted.q30.bam: ref.fasta ref.fasta.bwt
	if [ -n "$(SHORT_READ_PAIRED_FASTQ1)" ]; then \
	  $(BWA) mem -t $(PROCESSORS) $< $(SHORT_READ_PAIRED_FASTQ1) $(SHORT_READ_PAIRED_FASTQ2) | \
	  $(SAMTOOLS) view -q 30 -bS - | \
	  $(SAMTOOLS) sort - tmp.sorted; \
	elif [ -n "$(SHORT_READ_UNPAIRED_FASTQ)" ]; then \
	  $(BWA) mem -t $(PROCESSORS) $< $(SHORT_READ_UNPAIRED_FASTQ) | \
	  $(SAMTOOLS) view -q 30 -bS - | \
	  $(SAMTOOLS) sort - tmp.sorted; \
	fi
	mv tmp.sorted.bam $@

sr.sorted.q30.bam.bai: sr.sorted.q30.bam
	$(SAMTOOLS) index $<
