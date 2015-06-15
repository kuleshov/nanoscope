#!/usr/bin/env bash

# Clean previous installation
rm -r bin
rm celera soapdenovo AMOS spades cd-hit mummer FCP quast

set -e
cp -r src bin
cd bin

# COMPILE CELERA ASSEMBLER
# We are currently packaging Linux-64bit binaries
cd wgs-8.1
cd kmer && make install && cd ..
cd samtools && make && cd ..
cd src && make && cd ..
cd ..

# COMPILE SOAPDENOVO
cd ./SOAPdenovo2-src-r240 
make clean
make 
cd ..

# COMPILE CDHIT
cd ./cdhit-mod
make clean
make 
cd ..

# COMPILE MUMMER
cd ./MUMmer3.23-64bit-mod
# make clean
mkdir aux_bin
make check
make CPPFLAGS="-O3 -DSIXTYFOURBITS"
make install
MUMMERDIR=`pwd`
cd ..

# COMPILE AMOS
cd ./amos-3.1.0
# make clean
export NUCMER=$MUMMERDIR/nucmer
export DELTAFILTER=$MUMMERDIR/delta-filter
export SHOWCOORDS=$MUMMERDIR/show-coords
./configure
make 
make install
perl -pi -e s,"SHOWCOORDS\s+=.*,SHOWCOORDS=$MUMMERDIR/show-coords,g" bin/minimus2
perl -pi -e s,"NUCMER\s+=.*,NUCMER=$MUMMERDIR/nucmer,g" bin/minimus2
cd ..

# INSTALL FCP
cd ./FCP-1.0.5
python FCP_install.py
python BuildBlastDB.py makeblastdb ./training/sequences.txt
cd ..

cd ..
ln -s ./bin/wgs-8.1 celera
ln -s ./bin/SOAPdenovo2-src-r240 soapdenovo
ln -s ./bin/cdhit-mod cd-hit
ln -s ./bin/MUMmer3.23-64bit-mod mummer
ln -s ./bin/amos-3.1.0 AMOS
ln -s ./bin/FCP-1.0.5 FCP
ln -s ./bin/quast-2.3 quast
