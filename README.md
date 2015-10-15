Nanoscope
=========

Metagenomic analysis pipeline for synthetic long reads. Nanoscope was originally introduced in

```
High-resolution structure of the human microbiome revealed with synthetic long reads.
Volodymyr Kuleshov, Chao Jiang, Wenyu Zhou, Fereshteh Jahanbani, Serafim Batzoglou, Michael Snyder. 
Nature Biotechnology, 2015.
```

## Installation

### Requirements

Nanoscope assumes that the following basic UNIX and genomic analysis utilities be installed
on your system:

* GNU awk
* sed
* perl v5 or higher
* python v2
* GNU make
* GNU Parallel
* NCBI Blast >= 2.2.25
* BWA >= 0.7.5
* samtools >= 0.1.18
* bedtools >= 2.17.0
* pysam >= 0.8.2

The programs awk, perl, python, and blast must be in your `$PATH` during installation.
Paths to all the others can be specified at runtime.

The Nanoscope uses the following software in its analysis:

* Soapdenovo 2.04
* Celera assembler 8.1
* AMOS 3.1.0
* SPAdes 3.5.0
* Mummer 3.13 (modified)
* CD-Hit 4.6 (modified)
* FCP 1.0.5
* Quast 2.3
* Lens 1.0

The source code of these programs is part of the git repository;
it needs to be compiled during the installation process.
These programs' dependecies are part of a standard Linux setup;
if some dependecies are missing, you will be notified at installation time.

A Nanoscope installation uses approximately 50G of disk space.
Each Nanoscope run requires about 50G of disk space and 15G of RAM per long read 
library. Most stages can be parallelized, and we recommend using at least
16 cores.

In our experience, one run can take anywhere between one day (1 library, 10 cores) to one week
(7 libraries, 25 cores).

### Installing Nanoscope

Before installing Nanoscope, you need to make sure that
awk, perl, python, and makeblastdb are in your `$PATH`.
To install Nanoscope, clone the git repo and run 
the installation script for the third-party software:

```
git clone https://github.com/kuleshov/nanoscope.git;
cd nanoscope;
git submodule init;
git submodule update;
cd sw;
bash install.sh
```

The installation of third-party tools can take up to 5 hours.
The longest part is the installation of the FCP package,
which involves downloading the NCBI RefSeq genomes (7.5G)
and building their blast database.

The only package used by Nanoscope not included in the repository is
the optional SPAdes assembler. To compile SPAdes, the user needs the latest
version of several somewhat esoteric tools on which we do not want Nanoscope 
to depend. To use SPAdes, we ask the user to manually download binaries for 
their system, and add the appropriate path to the Nanoscope configuration.

### Testing the installation

To test whether the pipeline was installed succefully, we have provided a small testing package in 
`nanoscope/test`:

```
cd nanoscope/test;
make run;
```

This executes Nanoscope on a small subset of reads in fastq format.

## Running Nanoscope

Running the pipeline involves two steps: (1) creating and initializing
a new directory in which the run will take place; (2) starting the 
run with some additional run-time specific paramters.

Both of steps are done using the wrapper script `nanoscope.py`:

```
usage: nanoscope.py [-h] {status,init,run} ...

optional arguments:
  -h, --help         show this help message and exit

Commands:
  {status,init,run}
    init             Initialize pipeline
    run              Start/resume pipeline
    status           Display pipeline status
```

### Initializing a run directory

A run is initialized using the `init` command:

```
usage: nanoscope.py init [-h] -l LONG [-s SHORT_SINGLE]
                         [-p SHORT_PAIRED SHORT_PAIRED]
                         [-c CONTIGS [CONTIGS ...]]
                         [--short-insert-size SHORT_INSERT_SIZE]
                         [--short-read-length SHORT_READ_LENGTH] [--path PATH]
                         folder

positional arguments:
  folder                Pipeline folder

optional arguments:
  -h, --help            show this help message and exit
  -l LONG, --long LONG  Long reads fastq
  -s SHORT_SINGLE, --short-single SHORT_SINGLE
                        Short reads fastq (unpaired)
  -p SHORT_PAIRED SHORT_PAIRED, --short-paired SHORT_PAIRED SHORT_PAIRED
                        Short reads fastq (paired)
  -c CONTIGS [CONTIGS ...], --contigs CONTIGS [CONTIGS ...]
                        Pre-assembled contigs
  --short-insert-size SHORT_INSERT_SIZE
                        Short read insert size
  --short-read-length SHORT_READ_LENGTH
                        Short read insert size
  --path PATH           Path to nanoscope
```

During initialization, the user must specify input DNA sequences:

* A mandatory fastq file with long reads
* A highly recommended fastq file with short reads (paired-end or unpaired). Short reads are required for the abundance estimation stage.
* An optional set of pre-assembled contigs that will be merged with the assembled contigs

For example:
```
python bin/nanoscope.py init \
    -l test/reads.toy.long.fastq.gz \
    -s test/reads.toy.short.fastq \
    test/test-run
```

The folder `test/test-run` will be populated with folder containing
scripts that will launch various steps of the analysis.

The most important of these scipts is `test/test-run/config-and-run.sh`.
This file contains all the configuration parameters used across the pipeline.
They will all be set to sensible default values; advanced users however may
choose to customize this file. The most important options are:

* Paths to various programs
* Assembler options (see also `test-run/config-files` for that)
* Flags for turning off assembly merging or the entire assembly stage


### Starting a run

The `run` command starts a new run:

```
usage: nanoscope.py run [-h] [-p PROCESSORS] [-r] [--up-to UP_TO] [--skip-asm]
                        [--skip-minimus] [--spades]
                        folder

positional arguments:
  folder                Pipeline folder

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSORS, --processors PROCESSORS
                        Number of processors to use
  -r, --restart         Resume pipeline from the begginning
  --up-to UP_TO         Compute up to given stage
  --skip-asm            Skip read assembly
  --skip-minimus        Skip minimus contig merging
  --spades              Assemble short and long reads with spades
```

This executes the `config-and-run.sh` script in the run folder,
which sources the pipeline configuration settings and starts 
the pipeline scripts.

For example:
```
python bin/nanoscope.py run \
     -p 10 \
     test/test-run
```

The `run` command also supports additional options such as `--skip-asm` which skips
read assembly, `--skip-minimus`, which skips assembly merging, and `--up-to` which
runs the pipeline only up to a given stage. Finally, use `--spades` to assemble
both short and long reads using the SPAdes assembler; this produces longer contigs
but may assemble much fewer total sequence.

### Output

The output of Nanoscope will be found in the `results` subfolder.

Output includes:

- `asm.report.txt`: a Quast report of the assembly results 
- `taxa.abundances`: taxa identified by Nanoscope and their estimated abundances 
- `taxa.contig.assignments`: taxonomic labels of assembled contigs 
- `taxa.haplotypes`: bacterial haplotypes produced by Lens; see the Lens documentation for more info

## Feedback

Please send feedback to [Volodymyr Kuleshov](http://www.stanford.edu/~kuleshov).
