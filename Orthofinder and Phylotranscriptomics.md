**Orthofinder**

Finds orthologous proteins and generates orthogroups to create phylogenies. We use the MSA option Orthofinder to automatically generate a maximum likelihood tree based on multiple sequence alignment. This option requires fasttree in order to properly work.

```
#!/bin/bash
#SBATCH --job-name=OrthoFinder
#SBATCH --partition=compute
#SBATCH --mem=126G
#SBATCH --time=4-00:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mail-user=EMAIL
#SBATCH --mail-type=BEGIN,FAIL,END
#SBATCH --array 1

ml bioinfo-ugrp-modules
ml DebianMed/11.2
ml mafft
ml fasttree

# Increase the file descriptor limit
ulimit -n 4096  

# Run Orthofinder
/path/to/Orthofinder -f /path/to/peptides -M msa -o /path/to/desired/output_directory
```


