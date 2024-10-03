import pandas as pd 
from collections import defaultdict 
import sys 
import csv 
import gzip 
import argparse

def genome_file_to_gcf_acc(file_name):
    if 'ASM' in file_name:
        return file_name.split('/')[-1].split('_ASM')[0]
    return(file_name.split('/')[-1].split("_genomic")[0])

def contig_to_imgvr_acc(contig_name):
    return contig_name.split(' ')[0].split('|')[0]

parser = argparse.ArgumentParser(description='Convert a sylph output tsv file to a set of output files in MetaPhlAn format.')
parser.add_argument("-s", "--sylph", help="sylph output file", type=str, required=True)
parser.add_argument("-o", "--output-prefix", help="prefix of the outputs. Output files will be 'prefix + Sample_file_column + .sylphmpa'", type=str, default = "")
parser.add_argument("-m", "--metadata", help = "metadata file(s) converting genome files to taxonomic identifiers. Multiple input files will be concatenated.", type = str, required=True, nargs='+')
parser.add_argument("-a", "--annotate-virus-hosts", help = "add additional column(s) by integrating viral-host information available (currently available for IMGVR4.1)", action='store_true')
parser.add_argument("-f", "--add-folder-information", help = "include directory/folder information to the outputs. This is needed if your samples have the same read name but different directory structures.", action='store_true')
#add versioning
parser.add_argument('--version', action='version', version='%(prog)s 0.3')
args = parser.parse_args()
annotate_virus = args.annotate_virus_hosts

# Read sylph's output TSV file into a Pandas DataFrame
df = pd.read_csv(args.sylph, sep='\t')

### This is a dictionary that contains the genome_file 
### to taxonomy string mapping. It should be like
### {'my_genome.fna.gz' : b__Bacteria;...}
genome_to_taxonomy = dict()
genome_to_additional_data = dict()

print(f"Reading metadata files: {args.metadata} ...")

for file in args.metadata:
    ### Process gzip file instead if extension detected
    if '.gz' in file or '.gzip' in file:
        f=gzip.open(file,'rt')
    else:
        f = open(file,'r')

    ### Tag each taxonomy string with a t__ strain level identifier
    for row in f:
        spl = row.rstrip().split('\t');
        accession = spl[0]
        taxonomy = spl[1].rstrip() + ';t__' + accession
        if len(spl) > 2:
            genome_to_additional_data[accession] = spl[2].rstrip()
        genome_to_taxonomy[accession] = taxonomy

### Group by sample file. Output one file fo reach sample file. 
print(f"Processing sylph output file: {args.sylph} ...")
grouped = df.groupby('Sample_file')

outs = set()

for sample_file, group_df in grouped:
    first_warn = False
    if args.add_folder_information:
        out = '_'.join(sample_file.split('/'))
    else:
        out = sample_file.split('/')[-1]
    out_file = args.output_prefix + out + '.sylphmpa'
    print(f"Writing output to: {out_file} ...")
    if out_file in outs:
        print(f"ERROR! Multiple .sylphmpa files have the same sample name, which will cause a file to be overwritten. Consider --add-folder-information to disambiguate sample files")
        exit(1)
    outs.add(out_file)
    of = open(out_file,'w')

    tax_abundance = defaultdict(float)
    seq_abundance = defaultdict(float)
    ani_dict = defaultdict(float)
    cov_dict = defaultdict(float)

    # Iterate over each row in the DataFrame
    for idx, row in group_df.iterrows():
        if 'Genome_file' not in row or 'Contig_name' not in row or 'Adjusted_ANI' not in row or 'Sequence_abundance' not in row:
            print("ERROR: Missing required columns in sylph output file. Exiting.")
            sys.exit(1)

        # Parse the genome file... assume the file is in gtdb format.
        # This can be changed. 
        genome_file = genome_file_to_gcf_acc(row['Genome_file'])
        contig_id = contig_to_imgvr_acc(row['Contig_name'])
        ani = float(row['Adjusted_ANI'])
        if 'Eff_cov' in row:
            cov = float(row['Eff_cov'])
        else:
            cov = float(row['True_cov'])

        if genome_file in genome_to_taxonomy:
            tax_str = genome_to_taxonomy[genome_file]
        elif genome_file +'.gz' in genome_to_taxonomy:
            tax_str = genome_to_taxonomy[genome_file + '.gz']
        elif contig_id in genome_to_taxonomy:
            tax_str = genome_to_taxonomy[contig_id]
        else:
            tax_str = 'NO_TAXONOMY;t__' + genome_file
            if not first_warn:
                print(f"WARNING: No taxonomy information found for entry {genome_file} and contig {contig_id} in metadata files. Assigning default taxonomy")

        abundance = float(row['Sequence_abundance'])
        rel_abundance = float(row['Taxonomic_abundance'])

        # Split taxonomy string into levels and update abundance
        tax_levels = tax_str.split(';')
        cur_tax = ''
        for level in tax_levels:
            if cur_tax:
                cur_tax += '|'
            cur_tax += level
            tax_abundance[cur_tax] += rel_abundance
            seq_abundance[cur_tax] += abundance
            if 't__' in cur_tax:
                ani_dict[cur_tax] = ani
            if 't__' in cur_tax:
                cov_dict[cur_tax] = cov

    # Print the CAMI BioBoxes profiling format
    of.write(f"#SampleID\t{sample_file}\n")
    if annotate_virus:
        of.write("clade_name\trelative_abundance\tsequence_abundance\tANI (if strain-level)\t Coverage (if strain-level)\tVirus_host (if viral)\n")
    else:
        of.write("clade_name\trelative_abundance\tsequence_abundance\tANI (if strain-level)\t Coverage (if strain-level)\n")

    level_to_key = dict()
    for key in tax_abundance.keys():
        level = len(key.split('|'))
        if level not in level_to_key:
            level_to_key[level] = [key]
        else:
            level_to_key[level].append(key)

    sorted_keys = sorted(level_to_key.keys())

    for level in sorted_keys:
        keys_for_level = sorted(level_to_key[level], key = lambda x: tax_abundance[x], reverse=True)
        for tax in keys_for_level:
            if tax in ani_dict:
                if annotate_virus:
                    accession = tax.split('t__')[-1]
                    if accession in genome_to_additional_data:
                        val = genome_to_additional_data[accession]
                    else:
                        val = 'NA'
                    of.write(f"{tax}\t{tax_abundance[tax]}\t{seq_abundance[tax]}\t{ani_dict[tax]}\t{cov_dict[tax]}\t{val}\n")
                else:
                    of.write(f"{tax}\t{tax_abundance[tax]}\t{seq_abundance[tax]}\t{ani_dict[tax]}\t{cov_dict[tax]}\n")
            else:
                if annotate_virus:
                    of.write(f"{tax}\t{tax_abundance[tax]}\t{seq_abundance[tax]}\tNA\tNA\tNA\n")
                else:
                    of.write(f"{tax}\t{tax_abundance[tax]}\t{seq_abundance[tax]}\tNA\tNA\n")

