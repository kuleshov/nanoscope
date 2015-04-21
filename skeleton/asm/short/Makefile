# SHORT-READ ASSEMBLY USING SOAPDENOVO
# If short reads are given, assembles them into contigs.
# Input files: SHORT_READ_PAIRED_FASTQ1, SHORT_READ_PAIRED_FASTQ2, SHORT_READ_UNPAIRED_FASTQ
# Output file: short.fasta

#------------------------------------------------------------------------------
# High-level commands

all:
	if [ -n "$(SHORT_READ_PAIRED_FASTQ1)" ] ||  [ -n "$(SHORT_READ_UNPAIRED_FASTQ)" ]; then \
	make config.txt sparse-pregraph.done contig.done map.done scaff.done short.fasta; \
	else \
	make skip; \
	fi

skip:
	[ -e short.fasta ] || touch short.fasta

clean:
	-rm config.txt *.done short.fasta

#------------------------------------------------------------------------------
# Assembler instructions

config.txt: $(SHORT_READ_PAIRED_FASTQ1) $(SHORT_READ_PAIRED_FASTQ2) $(SHORT_READ_UNPAIRED_FASTQ)
	-rm config.txt
	if [ -n "$(SHORT_READ_PAIRED_FASTQ1)" ]; then \
	cat ../../config-files/soapdenovo.pai.template.txt >> config.txt && \
	echo q1=$(SHORT_READ_PAIRED_FASTQ1) >> config.txt && \
	echo q2=$(SHORT_READ_PAIRED_FASTQ2) >> config.txt && \
	echo avg_ins=$(SHORT_INS_SIZE) >> config.txt; \
	fi
	if [ -n "$(SHORT_READ_UNPAIRED_FASTQ)" ]; then \
	cat ../../config-files/soapdenovo.unp.template.txt >> config.txt && \
	echo q=$(SHORT_READ_UNPAIRED_FASTQ) >> config.txt; \
	fi

sparse-pregraph.done:
	$(SOAP) sparse_pregraph $(SP_PREGRAPH_OPT) -s config.txt -p $(PROCESSORS) -o short  1>pregraph.stdout 2>pregraph.stderr
	touch $@

contig.done:
	$(SOAP) contig -g short -p $(PROCESSORS) $(SP_CONTIG_OPT) 1>contig.stdout 2>contig.stderr
	touch $@

map.done:
	$(SOAP) map -s config.txt -g short -p $(PROCESSORS) $(SP_MAP_OPT) 1>map.stdout 2>map.stderr
	touch $@

scaff.done:
	$(SOAP) scaff -g short -p $(PROCESSORS) $(SP_SCAFF_OPT) 1>scaff.stdout 2>scaff.stderr
	touch $@

short.fasta: short.scafSeq
	ln -s $< $@
