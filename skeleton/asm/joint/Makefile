# COMBINING SHORT AND LONG READ ASSEMBLIES WITH MINIMUS2
# Input files: ../short/short.fasta ../long/long.fasta $(PRE_ASM_CONTIGS)
# Output file: joint.fasta

#------------------------------------------------------------------------------
# High-level commands

all.done all:
	if [ "$(SKIP_MINIMUS)" = "True" ]; then \
	make skip; \
	else \
	make joint.fasta; \
	fi
	touch all.done

skip:
	make ctgs.filtered.fasta
	ln -s ctgs.filtered.fasta joint.fasta
	touch all.done

clean:
	-rm *.fasta out.afg *.seq all.done

#------------------------------------------------------------------------------
# Assembler instructions

ctgs.fasta: ../short/short.fasta ../long/long.fasta $(PRE_ASM_CONTIGS)
	cat $^ > $@.tmp
	mv $@.tmp $@

ctgs.filtered.fasta: ctgs.fasta
	$(CDHIT) -i $< -o $@.tmp $(CDHITEST_OPT)
	mv $@.tmp $@

out.afg: ctgs.filtered.fasta
	$(AMOSDIR)/toAmos -s $< -o $@.tmp
	mv $@.tmp $@

out.fasta: out.afg
	$(AMOSDIR)/minimus2 out $(MINIMUS_OPT)

out.singletons.seq: out.fasta

joint.fasta: out.fasta out.singletons.seq
	cat $^ > $@.tmp
	mv $@.tmp $@
