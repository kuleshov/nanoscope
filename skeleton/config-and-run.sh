#!/bin/bash
set -e;

## NANOSCOPE CONFIGURATION FILE

# The settings of every program in the pipeline are stored in this file.
# Advanced users may edit these settings to fine

# ---------------------------------------------------------------------------
# Input

## Short reads:
# If an input type is not applicable, delete the variable or leave it as ""

# Fastq with paired short reads
export SHORT_READ_PAIRED_FASTQ1="{short_paired1}"
export SHORT_READ_PAIRED_FASTQ2="{short_paired2}"

# Fastq file with unpaired short reads:
export SHORT_READ_UNPAIRED_FASTQ="{short_unpaired}"

# Short read parameters
export SHORT_READ_LEN="{short_read_length}"
export SHORT_INS_SIZE="{short_insert_size}"

## Long reads:

# Fastq with long reads
export LONG_READ_FASTQ="{long}"

## Pre-assembled contig files:

# Fasta file with pre-assembled contigs
export PRE_ASM_CONTIGS="{contigs}"

# ---------------------------------------------------------------------------
# Program settings


## Assembly:

# Set this to "True" to skip assembly
# You must provide your own pre-assembled contigs in this case
export SKIP_ASM="False"

# Set this to "True" to jointly assemble short and long reads with SPAdes
export USE_SPADES="False"

# Soapdenovo settings:
# (see also ./config-files/soapdenovo.*.template.txt)

# the options below are added after each command
# (added in addition to -s config.txt -p $(PROCESSORS))
export SP_PREGRAPH_OPT="-K 51 -z 250000000 -R"
export SP_CONTIG_OPT=""
export SP_MAP_OPT=""
export SP_SCAFF_OPT="-F"

# Celera assembler settings:

# Library flags:
export CEL_LIB_FLAGS="-nonrandom -technology none -feature forceBOGunitigger 0 -feature doNotTrustHomopolymerRuns 0 -feature discardReadsWithNs 0 -feature doNotQVTrim 0 -feature deletePerfectPrefixes 0 -feature doNotOverlapTrim 0 -feature isNotRandom 0 -feature fastqQualityValues sanger"

# For all other options, see the spec file at: ./config-files/celera.spec

# SPAdes options:
export SPADES_OPT="--only-assembler -k 127 -m 100"

# Minimus2 settings:
# Set this to "True" to skip contig merging
export SKIP_MINIMUS="False"

export CDHITEST_OPT="-c 0.99 -M 3000"
export MINIMUS_OPT="-D OVERLAP=500"


## Classification:

# options for the LCA algorithm in FCP:
export LCA_OPT="1e-5 15"


## Subspecies detection:

# options for various stages of the Lens algorithm
# (these are added in addition to -p $(PROCESSORS))
export SMTLS_FILTER_OPT="-q 30"
export MK_VARIANTS_OPT=""
export MK_READS_OPT=""
export MK_HAPLOTYPES_OPT=""


## Abundance estimation:

# Resolution at which to report taxa:
# valid resolutions are STRAIN, SPECIES, GENUS, FAMILY, ORDER, CLASS, PHYLUM, DOMAIN
export RESOLUTION="GENUS"
# Cutoffs for calling a taxonomic unit as present in the metagenome:
# We call taxonomic units tha have at least TAX_BP_CUTOFF bp mapping to them
# within at least TAX_CTG_CUTOFF contigs.
export TAX_BP_CUTOFF=40000
export TAX_CTG_CUTOFF=5

# ---------------------------------------------------------------------------
# Paths

# Nanoscope paths

export NANOSCOPE="{nanoscope_path}"
export BIN="$NANOSCOPE/bin/"
export LENS="$BIN/lens/"

# Basic genomics tools

export AWK=`which awk`
export PARALLEL=`which parallel`
export PYTHON=`which python`
export BLASTN=`which blastn`
export BWA=`which bwa`
export SAMTOOLS=`which samtools`
export BT=`which bedtools`

# Assembly related software

export SOAP="$NANOSCOPE/sw/soapdenovo/SOAPdenovo-63mer"
export CELDIR="$NANOSCOPE/sw/celera/Linux-amd64/bin/"
export CDHIT="$NANOSCOPE/sw/cd-hit/cd-hit-est"
export AMOSDIR="$NANOSCOPE/sw/AMOS/bin/"
# the SPAdes assembler is not installed by default, you need
# to install it manually and connect it to Nanoscope:
export SPADES="$NANOSCOPE/sw/spades/bin/spades.py"

# Other programs

export FCPDIR="$NANOSCOPE/sw/FCP/"
export QUAST="$NANOSCOPE/sw/quast/quast.py"

# ---------------------------------------------------------------------------
# Make sure that every program exists!

test -a "$AWK" || (echo "Awk not found!" && exit 1)
test -a "$PARALLEL" || (echo "GNU Parallel not found!" && exit 1)
test -a "$PYTHON" || (echo "Python not found!" && exit 1)
test -a "$BLASTN" || (echo "Blastn not found!" && exit 1)
test -a "$BWA" || (echo "BWA not found!" && exit 1)
test -a "$SAMTOOLS" || (echo "Samtools not found!" && exit 1)
test -a "$BT" || (echo "Bedtools not found!" && exit 1)
test -a "$NANOSCOPE/sw" || (echo "Nanoscope third-party software folder not found!" && exit 1)
test -a "$BIN" || (echo "Nanoscope scripts folder not found!" && exit 1)

# ---------------------------------------------------------------------------
# Launch makefile

make "$@"
