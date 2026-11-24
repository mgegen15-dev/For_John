#!/usr/bin/env bash
# Engine cycle 2: download and unpack the public GEO files used by tools/engine_cycle02_cxcr4.py.
# About 1.5 GB. Run from the repository root. Files go to data/engine/cycle02/raw/ (not stored in git).
set -u
RAW=data/engine/cycle02/raw
F=https://ftp.ncbi.nlm.nih.gov/geo/series
mkdir -p "$RAW/x" && cd "$RAW"
get(){ [ -s "$2" ] || { sleep 3; curl -sS --retry 4 --retry-delay 5 -o "$2" "$1" || echo "FAILED $2"; }; }
get https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPLnnn/GPL96/annot/GPL96.annot.gz GPL96.annot.gz
get "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL3307&targ=self&form=text&view=data" GPL3307.platform.txt
get $F/GSE14nnn/GSE14359/matrix/GSE14359_series_matrix.txt.gz GSE14359_series_matrix.txt.gz
get $F/GSE32nnn/GSE32981/matrix/GSE32981_series_matrix.txt.gz GSE32981_series_matrix.txt.gz
get $F/GSE220nnn/GSE220538/suppl/GSE220538_tpm_metvsprimary_all.txt.gz GSE220538_tpm.txt.gz
get $F/GSE140nnn/GSE140131/suppl/GSE140131_Normalised_Reads.tsv.gz GSE140131_norm.tsv.gz
get $F/GSE237nnn/GSE237033/suppl/GSE237033_raw_counts.tsv.gz GSE237033_raw_counts.tsv.gz
get $F/GSE87nnn/GSE87624/suppl/GSE87624_Human_masked.txt.gz GSE87624_Human_masked.txt.gz
get $F/GSE318nnn/GSE318840/suppl/GSE318840_RAW.tar GSE318840_RAW.tar
get $F/GSE293nnn/GSE293065/suppl/GSE293065_RAW.tar GSE293065_RAW.tar
for b in BC2 BC3 BC5 BC6 BC10 BC16 BC17 BC21 BC22; do
  get $F/GSE152nnn/GSE152048/suppl/GSE152048_$b.matrix.tar.gz GSE152048_$b.tar.gz
  tar xzf GSE152048_$b.tar.gz -C x --exclude='._*' --exclude='.DS_Store'
done
tar xf GSE318840_RAW.tar -C x
tar xf GSE293065_RAW.tar -C x --wildcards '*.h5'
# A file of about 1 KB is an error page from the server: delete it and run again.
find . -maxdepth 1 -type f -size -2k ! -name '*.sh' -print | sed 's/^/CHECK (too small): /'
echo done
