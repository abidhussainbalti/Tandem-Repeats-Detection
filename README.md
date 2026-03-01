# NUST Genomics: Repeat Analysis
## Task 4 - Detecting Repetitive DNA Sequences in Primate Mitochondrial Genomes

---

## 📋 Project Overview

**Course:** Genomics (NUST)  
**Due Date:** March 4, 2026  
**Marks:** 10/100  
**Student:** Abid Hussain

### Objective
Identify and analyze repetitive DNA sequences in primate mitochondrial genomes using repeat detection analysis to understand evolutionary relationships and mutational hotspots.

---

## 📊 Dataset

Three complete mitochondrial genomes:
| Organism | Accession | Length | Source |
|----------|-----------|--------|--------|
| Human | NC_012920.1 | 16,569 bp | NCBI |
| Chimpanzee | NC_001643.1 | 16,554 bp | NCBI |
| Gorilla | NC_011120.1 | 16,412 bp | NCBI |

---

## 🔍 Repeat Detection Methodology

### Method Selection

**Originally Planned:** RepeatMasker (industry-standard tool)  
**Actually Used:** Custom Python-based repeat detection

**Rationale for Python Approach:**
- RepeatMasker configuration issues (FamDB library partitions, TRF integration)
- Python approach provides transparent, reproducible results
- Same biological insight with greater clarity
- Faster execution and easier customization

### Detection Criteria Explained

#### 1. **Tandem Repeats**

**Definition:** Short DNA sequences that repeat consecutively

**Parameters:**
- **Unit Length:** 2-6 bp (shortest repeat unit size)
- **Minimum Repeats:** 3+ consecutive copies required
- **Example:** CAG-CAG-CAG = tandem repeat (unit "CAG" repeated 3×)

**Detection Algorithm:**
```
For each sequence position:
  For each unit length (2-6 bp):
    Extract potential repeat unit
    Count how many times it repeats consecutively
    If count ≥ 3: Record as tandem repeat
```

**Biological Significance:**
- Indicates DNA polymerase slippage during replication
- Evolutionary instability hotspots
- Variable across species (indicates divergence)

#### 2. **Homopolymer Runs**

**Definition:** Long stretches of identical single base

**Parameters:**
- **Minimum Length:** 5+ consecutive identical bases
- **Bases Detected:** A, T, G, C
- **Examples:** AAAAA, TTTTT, GGGGGG, CCCCC

**Detection Algorithm:**
```
For each base (A, T, G, C):
  Find all stretches ≥ 5 consecutive copies
  Record position, base, and length
```

**Biological Significance:**
- Major mutation hotspots
- DNA polymerase error-prone regions
- Associated with microsatellite instability
- Relatively conserved across primates

#### 3. **Low-Complexity Regions**

**Definition:** Sequences with limited nucleotide diversity (AT-rich or GC-rich)

**Parameters:**
- **Window Size:** 20 bp sliding window
- **Complexity Threshold:** < 70% (fewer than 3 of 4 bases present)
- **Calculation:** (Unique bases in window) ÷ 4 × 100

**Examples:**
- AT-rich: ATATATATATATATATATAT = 50% complexity (only A, T)
- Mixed: ATGCATGCATGCATGCATGC = 100% complexity (all 4 bases)
- GC-rich: GCGCGCGCGCGCGCGCGCGC = 50% complexity (only G, C)

**Detection Algorithm:**
```
For each 20 bp window in sequence:
  Count unique bases (1-4 possible)
  Calculate complexity = unique_bases / 4
  If complexity < 0.70: Record as low-complexity region
```

**Biological Significance:**
- Indicate reduced functional constraint
- Show codon usage bias (coding regions)
- Evolutionary neutral regions
- Species-specific adaptation patterns

---

## 📈 Results Summary

### Comparative Analysis

| Metric | Human | Chimp | Gorilla |
|--------|-------|-------|---------|
| **Total BP** | 16,569 | 16,554 | 16,412 |
| **Tandem Repeats** | 112 | 96 | 138 |
| **Homopolymer Runs** | 114 | 117 | 124 |
| **Low-Complexity Regions** | 4 | 9 | 24 |
| **Total Repeat BP** | 1,324 | 1,196 | 1,576 |
| **Repeat Content %** | 7.99% | 7.22% | 9.60% |

### Key Findings

1. **Gorilla has highest repeat content** (9.60%)
   - Most tandem repeats (138)
   - Most low-complexity regions (24)
   - Indicates recent divergence and rapid evolution

2. **Human and Chimp similar** (7.99% vs 7.22%)
   - Close evolutionary relationship
   - Similar mutational patterns
   - Consistent with molecular clock

3. **Homopolymers conserved** (114-124 across all species)
   - Stable feature of mtDNA structure
   - Less variable between species
   - Suggests functional importance

### Biological Interpretation

**Why mtDNA has 7-10% repeats:**
- More compact than nuclear DNA
- Strong purifying selection against large repeats
- Functional constraints (protein-coding, rRNA, tRNA genes)
- Limited transposable element accumulation

**Species Differences:**
- Gorilla's higher repeat content suggests:
  - More recent effective population size
  - Accumulation of mutations over time
  - Less efficient selection against repeats
  - Possible accelerated evolution in certain regions

---

## 🚀 COMPLETE REPRODUCIBILITY GUIDE

### PART 1: Environment Setup

#### Step 1.1: Clone Repository
```bash
git clone https://github.com/yourusername/nust-genomics-repeat-analysis.git
cd nust-genomics-repeat-analysis
```

#### Step 1.2: Install Python Dependencies
```bash
pip install -r requirements.txt
# Or manually:
pip install pandas matplotlib seaborn
```

---

### PART 2: Download Sequences

#### Step 2.1: Download mtDNA from NCBI
```bash
cd inputs/

# Human mtDNA
wget -O human_mtdna.fasta \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=NC_012920.1&rettype=fasta&retmode=text"

# Chimp mtDNA
wget -O chimp_mtdna.fasta \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=NC_001643.1&rettype=fasta&retmode=text"

# Gorilla mtDNA
wget -O gorilla_mtdna.fasta \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=NC_011120.1&rettype=fasta&retmode=text"

# Verify
ls -lh *.fasta
```

---

### PART 3: Run Repeat Analysis

#### Step 3.1: Run Python Analysis
```bash
cd ../scripts/

# Execute repeat detection
python3 02_python_repeat_analysis.py

# Output: repeat_detection_summary.csv saved to results/analysis/
```

#### Step 3.2: Verify Results
```bash
cd ../results/analysis/
cat repeat_detection_summary.csv
```

---

### PART 4: Analyze Results (Optional: Google Colab)

#### Step 4.1: Create Visualizations
```python
import pandas as pd
import matplotlib.pyplot as plt

# Read results
df = pd.read_csv('repeat_detection_summary.csv')

# Create comparison charts
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Repeat Content %
axes[0,0].bar(df['Species'], df['Repeat %'], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[0,0].set_title('Repeat Content % Comparison')
axes[0,0].set_ylabel('Repeat %')

# Chart 2: Tandem Repeats
axes[0,1].bar(df['Species'], df['Tandem Repeats'], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[0,1].set_title('Tandem Repeats Found')
axes[0,1].set_ylabel('Count')

# Chart 3: Homopolymers
axes[1,0].bar(df['Species'], df['Homopolymers'], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[1,0].set_title('Homopolymer Runs Found')
axes[1,0].set_ylabel('Count')

# Chart 4: Low-Complexity Regions
axes[1,1].bar(df['Species'], df['Low-Complexity Regions'], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[1,1].set_title('Low-Complexity Regions')
axes[1,1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('repeat_analysis_comparison.png', dpi=300)
plt.show()
```

---

## ✅ Verification Checklist
```
✅ inputs/
   ✅ human_mtdna.fasta (17K)
   ✅ chimp_mtdna.fasta (17K)
   ✅ gorilla_mtdna.fasta (17K)

✅ scripts/
   ✅ 02_python_repeat_analysis.py

✅ results/analysis/
   ✅ repeat_detection_summary.csv

✅ README.md
✅ METHODOLOGY.md (this file)
✅ requirements.txt
✅ .gitignore
```

---

## 🔧 Troubleshooting

### Issue: FASTA files not found
```bash
cd inputs/
# Re-download using wget commands above
```

### Issue: Python script fails
```bash
# Check Python version
python3 --version

# Install pandas if missing
pip install pandas
```

### Issue: Results file not created
```bash
# Check write permissions
ls -l results/analysis/
chmod 755 results/analysis/
# Re-run script
python3 02_python_repeat_analysis.py
```

---

## 📊 Expected Runtime

| Task | Time |
|------|------|
| Download sequences | 1-2 min |
| Run Python analysis | < 1 min |
| Create visualizations | 2-3 min |
| **Total** | **5-10 min** |

---

## 📚 References

1. Benson, G. (1999). Tandem repeats finder: A program to analyze DNA sequences. *Nucleic Acids Research*, 27(2), 573-580.
2. Altschul, S.F., et al. (1990). Basic local alignment search tool. *J Mol Biol*, 215(3), 403-410.
3. NCBI Nucleotide Database: https://www.ncbi.nlm.nih.gov/nucleotide/

---

## ✍️ Author
**Abid Hussain** | NUST Genomics | March 1, 2026

---

## 📊 Generated Output Files

### Visualization Results
- **repeat_analysis_comparison.png** (405 KB)
  - 4 comparative charts showing repeat analysis across 3 species
  - Generated from Google Colab analysis
  - Shows: Repeat %, Tandem Repeats, Homopolymers, Summary Table

### Data Results
- **repeat_detection_summary.csv**
  - Complete analysis metrics for all 3 species
  - Columns: Species, Total BP, Tandem Repeats, Homopolymers, Low-Complexity Regions, Total Repeat BP, Repeat %

### Example Output
```
Species,Total BP,Tandem Repeats,Homopolymers,Low-Complexity Regions,Total Repeat BP,Repeat %
Human,16569,112,114,4,1324,7.99
Chimp,16554,96,117,9,1196,7.22
Gorilla,16412,138,124,24,1576,9.6
```

