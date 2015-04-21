## TEST THE NANOSCOPE PACKAGE

run:
	python ../bin/nanoscope.py init \
	  -l ./reads.toy.long.fastq.gz \
	  -p ./reads.toy.short.1.fastq.gz ./reads.toy.short.2.fastq.gz \
	  test-run
	cp celera.test.spec test-run/config-files/celera.spec
	sed -i '/export TAX_BP_CUTOFF=40000/c\export TAX_BP_CUTOFF=10000' test-run/config-and-run.sh
	sed -i '/export TAX_CTG_CUTOFF=5/c\export TAX_CTG_CUTOFF=1' test-run/config-and-run.sh
	python ../bin/nanoscope.py run \
	   -p 10 \
	   test-run


clean:
	-rm -r test-run
