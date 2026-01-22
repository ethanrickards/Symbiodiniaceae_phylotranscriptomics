import os
import subprocess
import sys
import csv


# FUNCTIONS

def run_blast(query_file, db, output_file, perc_identity):
    """Run BLAST and save tabular results with % identity filter."""
    blast_command = [
        "blastn",
        "-query", query_file,
        "-db", db,
        "-out", output_file,
        "-outfmt", "6 qseqid sseqid pident length qcovs",
        "-perc_identity", str(perc_identity),
        "-num_threads", "4"
    ]
    subprocess.run(blast_command, check=True)

def parse_blast_results(blast_file):
    """
    Parse BLAST output.
    Returns:
      num_queries_with_hits (int),
      num_unique_subjects (int)
    """
    hits_by_query = {}
    unique_subjects = set()

    with open(blast_file, "r") as infile:
        for line in infile:
            cols = line.strip().split("\t")
            if len(cols) < 2:
                continue
            qseqid, sseqid = cols[0], cols[1]
            hits_by_query[qseqid] = True
            unique_subjects.add(sseqid)

    num_queries_with_hits = len(hits_by_query)
    num_unique_subjects = len(unique_subjects)
    return num_queries_with_hits, num_unique_subjects

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# SCRIPT

def main():
    if len(sys.argv) != 5:
        print("Usage: python script.py <orthogroup_dir> <genome_db_prefix> <output_dir> <perc_identity>")
        sys.exit(1)

    orthogroup_dir = sys.argv[1]
    db_prefix = sys.argv[2]      # Make sure this is a SINGLE Concatenated Blast Database
    output_dir = sys.argv[3]
    perc_identity = float(sys.argv[4])

    ensure_dir(output_dir)
    summary_file = os.path.join(output_dir, "orthogroup_concat_summary.csv")

    with open(summary_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow([
            "Orthogroup", "Database",
            "Query_Sequences_With_Matches", "Unique_Matches_Total"
        ])

        # Loop over orthogroups
        for og_file in sorted(os.listdir(orthogroup_dir)):
            if not og_file.endswith(".fa"):
                continue
            og_path = os.path.join(orthogroup_dir, og_file)
            og_name = os.path.splitext(og_file)[0]

            # Run Blast
            blast_output = os.path.join(output_dir, f"{og_name}_vs_concat.blast")
            run_blast(og_path, db_prefix, blast_output, perc_identity)

            # Parse BLAST results
            num_queries_with_hits, num_unique_subjects = parse_blast_results(blast_output)

            # Write row
            writer.writerow([
                og_name, os.path.basename(db_prefix),
                num_queries_with_hits, num_unique_subjects
            ])

    print(f"Summary written to {summary_file}")


if __name__ == "__main__":
    main()
