#!/usr/bin/env python3
"""
Analyze RepeatMasker output - Calculate repeat statistics
"""

import sys
from pathlib import Path

def analyze_masked_sequence(fasta_file, species_name):
    """Calculate repeat content from masked sequence"""
    
    total_bp = 0
    masked_bp = 0
    lowercase_count = 0
    uppercase_count = 0
    
    with open(fasta_file, 'r') as f:
        in_seq = False
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                in_seq = True
                continue
            if in_seq:
                total_bp += len(line)
                # Count lowercase (masked repeats)
                lowercase_count += sum(1 for c in line if c.islower())
                # Count uppercase (unmasked)
                uppercase_count += sum(1 for c in line if c.isupper())
    
    repeat_pct = (lowercase_count / total_bp * 100) if total_bp > 0 else 0
    
    return {
        'Species': species_name,
        'Total BP': total_bp,
        'Masked BP': lowercase_count,
        'Unmasked BP': uppercase_count,
        'Repeat %': round(repeat_pct, 2)
    }

# Analyze all three species
results = []
results.append(analyze_masked_sequence('../results/masked_sequences/human_mtdna.masked', 'Human'))
results.append(analyze_masked_sequence('../results/masked_sequences/chimp_mtdna.masked', 'Chimp'))
results.append(analyze_masked_sequence('../results/masked_sequences/gorilla_mtdna.masked', 'Gorilla'))

# Display results
print("\n" + "="*70)
print("REPEATMASKER ANALYSIS - REPEAT CONTENT COMPARISON")
print("="*70)
print()
for r in results:
    print(f"{r['Species']}:")
    print(f"  Total BP: {r['Total BP']:,}")
    print(f"  Masked BP (Repeats): {r['Masked BP']:,}")
    print(f"  Unmasked BP: {r['Unmasked BP']:,}")
    print(f"  Repeat Content: {r['Repeat %']}%")
    print()

print("="*70)

# Save to CSV
import csv
with open('../results/analysis/repeat_summary.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['Species', 'Total BP', 'Masked BP', 'Unmasked BP', 'Repeat %'])
    writer.writeheader()
    writer.writerows(results)

print("✅ Results saved to: results/analysis/repeat_summary.csv")
