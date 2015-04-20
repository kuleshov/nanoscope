#!/usr/bin/env bash
set -e

# COMPILE CELERA ASSEMBLER
# We are currently packaging Linux-64bit binaries
ln -s ./wgs-8.1 celera

# COMPILE SOAPDENOVO
cd ./SOAPdenovo2-src-r240 
make clean
make 
ln -s ./SOAPdenovo2-src-r240 soapdenovo
cd ..

# COMPILE CDHIT
cd ./cdhit-mod
make clean
make 
ln -s ./cdhit-mod cd-hit
cd ..

# COMPILE MUMMER
cd ./MUMmer3.23-64bit-mod
make clean
make check
make CPPFLAGS="-O3 -DSIXTYFOURBITS"
make install
MUMMERDIR=`pwd`
ln -s ./MUMmer3.23-64bit-mod mummer
cd ..

# COMPILE AMOS
cd ./amos-3.1.0
make clean
export NUCMER=$MUMMERDIR/nucmer
./configure
make 
make install
perl -pi -e s,"SHOWCOORDS\s+=.*,SHOWCOORDS=$MUMMERDIR/show-coords,g" bin/minimus2
perl -pi -e s,"NUCMER\s+=.*,NUCMER=$MUMMERDIR/nucmer,g" bin/minimus2
ln -s ./amos-3.1.0 AMOS
cd ..

# INSTALL FCP
cd ./FCP-1.0.5
ln -s ./FCP-1.0.5 FCP
python FCP_install.py
python BuildBlastDB.py makeblastdb ./training/sequences.txt
