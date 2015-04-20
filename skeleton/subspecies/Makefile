# UNCOVERS HAPLOTYPES IN BACTERIAL CONTIGS USING LENS
# Input files: ../asm/contigs.fasta, LONG_READ_FASTQ
# Output files: haplotypes.txt

#------------------------------------------------------------------------------
# High-level commands

all.done all:
	make align.done detect.done
	touch $@

clean:
	-rm *.done

#------------------------------------------------------------------------------
# Substages

align.done:
	make -C align
	touch $@

detect.done: align.done
	make -C detect
