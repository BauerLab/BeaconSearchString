#!/bin/sh

shopt -s extglob
mkdir tempFolder
awk 'BEGIN {n_seq=0;} /^>/ {if(n_seq%1==0){file=sprintf("tempFolder/myseq%d.fa",n_seq);} print > file; n_seq++; next;} { print >> file; }' < $1
for filename in tempFolder/myseq+([0-9]).fa; do
	cat reference.fa >> $filename
	mafft-mac/mafft.bat --quiet $filename > ${filename}_alignment.txt
done
python3 aligner.py
rm -R tempFolder