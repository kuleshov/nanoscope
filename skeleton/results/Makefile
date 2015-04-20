# COMPILATION OF FINAL RESULTS FROM A NANOSCOPE RUN
# Input files: All previous stages must be completed

all.done all:
	make quast taxa haplotypes
	touch all.done

clean:
	-rm -r all.done contigs.fasta asm.report.txt taxa.*

quast:
	ln -s ../asm/contigs.fasta
	$(QUAST) contigs.fasta
	ln -s quast_results/latest/report.txt asm.report.txt

taxa:
	ln -s ../classify/lca.results taxa.contig.assigments
	ln -s ../abundance/detect/taxa.abundances

haplotypes:
	ln -s ../subspecies/detect/haplotypes.txt taxa.haplotypes

