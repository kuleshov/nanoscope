# COMBINING SHORT AND LONG READ ASSEMBLIES WITH MINIMUS2
# Input files: CTGS
# Output files: lca.results lca.summary

SHELL=/bin/bash -e -o pipefail

#------------------------------------------------------------------------------
# High-level commands

CTGS:=../asm/contigs.fasta

all:
	make lca.summary

clean:
	-rm ctgs.split.* *.results lca.*

#------------------------------------------------------------------------------
# Details

blast_data: $(FCPDIR)/blast_data
	ln -s $<

taxonomy.txt: $(FCPDIR)/taxonomy.txt
	ln -s $<

blastn.results: $(CTGS) blast_data taxonomy.txt
	-rm -f ctgs.split.*
	cat $(CTGS) | python $(BIN)/format-fasta.py | split -d -l 1000 - ctgs.split.
	ls ctgs.split* | $(PARALLEL) -j $(PROCESSORS) $(PYTHON) $(FCPDIR)/BLASTN.py $(BLASTN) {} {}.blastn.results
	test -s ctgs.split.00.blastn.results
	cat ctgs.split.*.blastn.results > $@.tmp
	rm *.split.*
	mv $@.tmp $@

lca.results: blastn.results
	$(PYTHON) $(FCPDIR)/LCA.py $< $(LCA_OPT) $@.tmp
	mv $@.tmp $@

lca.summary: lca.results
	$(PYTHON) $(FCPDIR)/TaxonomicSummary.py $(CTGS) $< $@.tmp
	mv $@.tmp $@
