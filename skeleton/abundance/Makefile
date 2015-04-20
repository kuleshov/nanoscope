# UNCOVERS HAPLOTYPES IN BACTERIAL CONTIGS USING LENS
# Input files: CTGS, CONTIG_CLASSIFICATION, TAXONOMIC_CLASSIFICATION
# Output files: taxa.abundances

#------------------------------------------------------------------------------
# High-level commands

all.done all:
	make align.done detect.done
	touch $@

clean:
	-rm *.done
	make -C align clean
	make -C detect clean

SELF_DIR:=$(dir $(lastword $(MAKEFILE_LIST)))

#------------------------------------------------------------------------------
# SUBSTAGES

align.done:
	make -C align
	touch $@

detect.done:
	make -C detect
	  # CONTIG_CLASSIFICATION=$(CONTIG_CLASSIFICATION) \
	  # TAXONOMIC_CLASSIFICATION=$(TAXONOMIC_CLASSIFICATION) \
	  # SHORT_READ_ALIGNMENT=$(SHORT_READ_ALIGNMENT)
	touch $@
