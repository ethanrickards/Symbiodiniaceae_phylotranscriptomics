import os
import sys

def extract_transcripts(orthogroup_file, transcriptome_dir, output_file):
    # Read the sequence headers
    with open(orthogroup_file, 'r') as og_file:
        sequence_headers = [line.strip().lstrip('>') for line in og_file if line.startswith('>')]
    
    # Create a set for faster lookup
    sequence_set = set(sequence_headers)
    
    with open(output_file, 'w') as out_file:
        # Iterate through each FASTA file in the transcriptome directory
        for fasta_file in os.listdir(transcriptome_dir):
            if fasta_file.endswith('.fasta') or fasta_file.endswith('.fa'):
                with open(os.path.join(transcriptome_dir, fasta_file), 'r') as infile:
                    write_transcript = False
                    for line in infile:
                        if line.startswith('>'):
                            header = line.strip().lstrip('>')
                            if header in sequence_set:
                                write_transcript = True
                                out_file.write(line)
                            else:
                                write_transcript = False
                        elif write_transcript:
                            out_file.write(line)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python extract_transcripts.py <orthogroup_file> <transcriptome_directory> <output_file>")
        sys.exit(1)

    orthogroup_file = sys.argv[1]
    transcriptome_dir = sys.argv[2]
    output_file = sys.argv[3]

    extract_transcripts(orthogroup_file, transcriptome_dir, output_file)
