# USES THE LENS ALGORITHM TO PRODUCE BACTERIAL HAPLOTYPES WITHIN CONTIGS
# Input files: BAM
# Output files: haplotypes.txt

#------------------------------------------------------------------------------
# High-level commands

all:
	make haplotypes.txt

clean:
	-rm *.done *.bam.* variants.* haplotypes.txt

#------------------------------------------------------------------------------
# Alignment process

BAM:=../align/lr.sorted.bam

filtered.bam: $(BAM)
	$(PYTHON) $(LENS)/filter_by_cigar.py -i $< -o $@.tmp
	mv $@.tmp $@

filtered.q30.bam: filtered.bam
	$(SAMTOOLS) view -h $(SMTLS_FILTER_OPT)  $< | $(SAMTOOLS) view -bS - > $@.tmp
	mv $@.tmp $@

filtered.q30.bam.bai: filtered.q30.bam
	$(SAMTOOLS) index $<

variants.pos: filtered.q30.bam filtered.q30.bam.bai
	python $(LENS)/make_variants.py -b $< -p $(PROCESSORS) -o $@.tmp $(MK_VARIANTS_OPT)
	mv $@.tmp $@

variants.reads: filtered.q30.bam filtered.q30.bam.bai variants.pos
	python $(LENS)/make_reads.py -b $< -p $(PROCESSORS) -v variants.pos -r $@.tmp $(MK_READS_OPT)
	mv $@.tmp $@

haplotypes.txt: filtered.q30.bam variants.pos variants.reads
	python $(LENS)/detect_subspecies.py -b $< -p $(PROCESSORS) -r variants.reads -k $@.tmp $(MK_HAPLOTYPES_OPT)
	mv $@.tmp $@
