#!/usr/bin/env python3
"""
Python-based Repeat Detection for mtDNA
Detects: tandem repeats, microsatellites, homopolymer runs, low-complexity regions
"""

import re
from collections import defaultdict

def find_tandem_repeats(seq, min_unit=2, max_unit=6):
    """Find tandem repeats in sequence"""
    repeats = []
    for unit_len in range(min_unit, max_unit + 1):
        for i in range(len(seq) - unit_len):
            unit = seq[i:i+unit_len]
            # Look for repeats of this unit
            count = 1
            j = i + unit_len
            while j + unit_len <= len(seq) and seq[j:j+unit_len] == unit:
                count += 1
                j += unit_len
            if count >= 3:  # At least 3 repeats
                repeats.append({
                    'type': 'tandem',
                    'position': i,
                    'unit': unit,
                    'length': unit_len,
                    'count': count,
                    'total_bp': count * unit_len
                })
    return repeats

def find_homopolymers(seq, min_length=5):
    """Find homopolymer runs (AAAA, TTTT, etc.)"""
    homopolymers = []
    bases = ['A', 'T', 'G', 'C']
    for base in bases:
        pattern = base * min_length
        for match in re.finditer(pattern, seq):
            length = len(match.group())
            homopolymers.append({
                'type': 'homopolymer',
                'position': match.start(),
                'base': base,
                'length': length
            })
    return homopolymers

def find_low_complexity(seq, window=20, threshold=0.7):
    """Find low-complexity regions"""
    low_complexity = []
    for i in range(len(seq) - window):
        window_seq = seq[i:i+window]
        unique_bases = len(set(window_seq))
        complexity = unique_bases / 4  # 4 possible bases
        if complexity < threshold:
            low_complexity.append({
                'type': 'low_complexity',
                'position': i,
                'length': window,
                'complexity': round(complexity, 2)
            })
    return low_complexity

def analyze_sequence(fasta_file, species_name):
    """Complete repeat analysis"""
    # Read FASTA
    seq = ''
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue
            seq += line.strip().upper()
    
    total_bp = len(seq)
    
    # Find repeats
    tandem = find_tandem_repeats(seq)
    homopolymers = find_homopolymers(seq)
    low_complexity_regions = find_low_complexity(seq)
    
    # Calculate repeat content
    repeat_bp = 0
    for rep in tandem:
        repeat_bp += rep['total_bp']
    for hp in homopolymers:
        repeat_bp += hp['length']
    
    repeat_pct = (repeat_bp / total_bp * 100) if total_bp > 0 else 0
    
    return {
        'species': species_name,
        'total_bp': total_bp,
        'tandem_repeats': len(tandem),
        'homopolymers': len(homopolymers),
        'low_complexity_regions': len(low_complexity_regions),
        'total_repeat_bp': repeat_bp,
        'repeat_pct': round(repeat_pct, 2),
        'tandem_details': tandem[:5],  # Top 5
        'homopolymer_details': homopolymers[:5]
    }

# Analyze all three species
print("\n" + "="*80)
print("PYTHON-BASED REPEAT DETECTION ANALYSIS - Primate mtDNA")
print("="*80)

results = []
files = [
    ('../inputs/human_mtdna.fasta', 'Human'),
    ('../inputs/chimp_mtdna.fasta', 'Chimp'),
    ('../inputs/gorilla_mtdna.fasta', 'Gorilla')
]

for fasta_file, species in files:
    try:
        result = analyze_sequence(fasta_file, species)
        results.append(result)
        
        print(f"\n{species} mtDNA Analysis:")
        print(f"  Total BP: {result['total_bp']:,}")
        print(f"  Tandem Repeats Found: {result['tandem_repeats']}")
        print(f"  Homopolymer Runs Found: {result['homopolymers']}")
        print(f"  Low-Complexity Regions: {result['low_complexity_regions']}")
        print(f"  Total Repeat BP: {result['total_repeat_bp']:,}")
        print(f"  Repeat Content: {result['repeat_pct']}%")
        
    except Exception as e:
        print(f"Error processing {species}: {e}")

print("\n" + "="*80)

# Save to CSV
import csv
with open('../results/analysis/repeat_detection_summary.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Species', 'Total BP', 'Tandem Repeats', 'Homopolymers', 
                     'Low-Complexity Regions', 'Total Repeat BP', 'Repeat %'])
    for r in results:
        writer.writerow([r['species'], r['total_bp'], r['tandem_repeats'], 
                        r['homopolymers'], r['low_complexity_regions'], 
                        r['total_repeat_bp'], r['repeat_pct']])

print("✅ Analysis complete!")
print("✅ Results saved to: results/analysis/repeat_detection_summary.csv")
