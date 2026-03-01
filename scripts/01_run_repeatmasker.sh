#!/bin/bash
# Script: Run RepeatMasker on mtDNA sequences
# Author: Abid Hussain
# Date: March 1, 2026

REPEATMASKER="/home/abidhussain/RepeatMasker/RepeatMasker"

echo "======================================"
echo "Running RepeatMasker Analysis"
echo "======================================"

cd ../results/masked_sequences

# Run RepeatMasker on Human mtDNA
echo "Processing Human mtDNA..."
$REPEATMASKER -species human \
              -q \
              -dir . \
              -a \
              ../../inputs/human_mtdna.fasta > ../../logs/repeatmasker_human.log 2>&1

# Run RepeatMasker on Chimp mtDNA
echo "Processing Chimp mtDNA..."
$REPEATMASKER -species "Pan troglodytes" \
              -q \
              -dir . \
              -a \
              ../../inputs/chimp_mtdna.fasta > ../../logs/repeatmasker_chimp.log 2>&1

# Run RepeatMasker on Gorilla mtDNA
echo "Processing Gorilla mtDNA..."
$REPEATMASKER -species "Gorilla gorilla" \
              -q \
              -dir . \
              -a \
              ../../inputs/gorilla_mtdna.fasta > ../../logs/repeatmasker_gorilla.log 2>&1

echo ""
echo "RepeatMasker analysis completed!"
echo ""
echo "Output files created:"
ls -lh *.out *.masked 2>/dev/null | awk '{print "  - " $NF}'

echo "======================================"
