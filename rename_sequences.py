import sys

def extract_between_double_underscores(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                # Keep everything between the first and last double underscore
                parts = line.strip().split('__')
                if len(parts) > 2:
                    simplified_header = parts[1]
                else:
                    simplified_header = line.strip()
                # Write the simplified header
                outfile.write(f">{simplified_header}\n")
            else:
                # Retain the sequence
                outfile.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.fasta output.fasta")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    extract_between_double_underscores(input_file, output_file)
