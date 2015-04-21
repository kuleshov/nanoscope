# ABUNDANCE ESTIMATION FROM SHORT READS
# Input files: CONTIG_CLASSIFICATION, TAXONOMIC_CLASSIFICATION, SHORT_READ_ALIGNMENT
# Output files: taxa.abundances

#------------------------------------------------------------------------------
# High-level commands

all:
	make taxa.abundances

clean:
	-rm taxa.* ctg.*

#------------------------------------------------------------------------------
# Abundance estimation

CONTIG_CLASSIFICATION:=../../classify/lca.results
TAXONOMIC_CLASSIFICATION:=../../classify/lca.summary
SHORT_READ_ALIGNMENT:=../align/sr.sorted.q30.bam

taxa.suspected: $(TAXONOMIC_CLASSIFICATION)
	$(PYTHON) $(BIN)/select_present_taxa.py \
	  --tax $< \
	  --res $(RESOLUTION) \
	  --bp-cutoff $(TAX_BP_CUTOFF) \
	  --ctg-cutoff $(TAX_CTG_CUTOFF) \
	  --present $@.tmp
	mv $@.tmp $@

ctg.coverages: $(SHORT_READ_ALIGNMENT)
	$(SAMTOOLS) idxstats $< > $@.tmp
	mv $@.tmp $@

taxa.abundances: taxa.suspected $(CONTIG_CLASSIFICATION) ctg.coverages
	$(PYTHON) $(BIN)/determine_abundances.py \
	  --taxa $< \
	  --ctgs $(CONTIG_CLASSIFICATION) \
	  --cov ctg.coverages \
	  --res $(RESOLUTION) \
	  --read-len $(SHORT_READ_LEN) \
	  --abundances $@.tmp
	mv $@.tmp $@


