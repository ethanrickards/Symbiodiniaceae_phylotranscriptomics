Separation of Symbiodiniaceae from host sea anemone transcripts via Kraken2.  In order to do this, use reference transcriptomes of Symbiodiniaceae and host species.  
For this study, we used the following transcriptomes for Symbiodiniaceae:

```
Breviolum pseudominutum - Parkinson et al. 2016, 
Durusdinium trenchii - Chen et al. 2023, https://espace.library.uq.edu.au/view/UQ:2692e99
Cladocopium goreauii - Shoguchi et al. 2018
Symbiodinium microadriaticum - Aranda et al. 2016
```

The use of additional transcriptomes of both host and dinoflagellate may influence separation.  These four transcriptomes, along with seven transcriptomes of host anemones, provided a clean separation between anemone and Symbiodiniaceae transcripts.  Note that Kraken2 typically operates with genomes, though we found no issue using transcriptomes.

You will need to build your Kraken2 database by hand, though this is fairly simple.  For each of your reference transcriptomes, you need to ensure each of your sequences has an ID. This can be accomplished by adding "kraken:taxid|XXX" in the sequence ID, where XXX is the taxon ID. taxon IDs are found via NCBI.  For more information, refer to the github on Kraken2: https://github.com/DerrickWood/kraken2/wiki/Manual

After modifying each of your references, create a database of your references through

```
kraken2-build --add-to-library REFERENCE.fa --db $DBNAME
```

After each of your references are added to the library, build using the following:

```
kraken2-build --build --db REFERENCE_db --threads 16
```

This should create your database for separation.  We can then use this for further separation.

```
#!/bin/bash
#SBATCH --job-name=kraken2_analysis
#SBATCH --partition=compute
#SBATCH --mem=32G
#SBATCH --time=1-00:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=insert_email@X.X
#SBATCH --output=Kraken2_%A.out
#SBATCH --error=kraken2_%A.err
#SBATCH --mail-type=BEGIN,FAIL,END
#SBATCH --array=1

ml bioinfo-ugrp-modules
ml DebianMed/11.2
ml salmon
ml sra-tools
ml kraken2

export IN_DIR="/location/of/cleaned_and_renamed/transcripts"
for file in $IN_DIR/*_Trinity.fasta.mod02; do
  filename=$(basename -- "$file")
		filename_no_ext="${filename%.*}"
		kraken2 --db DBNAME_db \
			--report ${filename_no_ext}_kraken2_report.txt \
			--use-mpa-style \
			--output ${filename_no_ext}_kraken2_output.txt \
			--classified-out ${filename_no_ext}_SymAnem_classified_sequences.fasta \
      "${file}"
		#remove the Kraken Label	
		awk '/^>/ {p=index($0,"kraken:taxid|") && ($0 ~ /kraken:taxid\|2499525|kraken:taxid\|2562237|kraken:taxid\|1381693|kraken:taxid\|2951/)} p' ${filename_no_ext}_SymAnem_classified_sequences.fasta > ${filename_no_ext}_filtered.fasta
		sed 's/ kraken:taxid|[0-9]*//' ${filename_no_ext}_filtered.fasta > ${filename_no_ext}_SymAnem_Krakenout.fasta
	done
```

This should generate f
