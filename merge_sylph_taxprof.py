import argparse
import pandas as pd

def read_tsv(file_path, column_name):
    df = pd.read_csv(file_path, sep='\t', usecols=['clade_name', column_name], comment='#')
    df.set_index('clade_name', inplace=True)
    return df

def merge_data(files, column_name):
    merged_df = pd.DataFrame()
    if column_name == 'ANI':
        column_name = 'ANI (if strain-level)'
    for file in files:
        df = read_tsv(file, column_name)
        df.rename(columns={column_name: file}, inplace=True)
        if merged_df.empty:
            merged_df = df
        else:
            merged_df = merged_df.join(df, how='outer')
    merged_df.fillna(0, inplace=True)
    return merged_df

def main():
    parser = argparse.ArgumentParser(description="Merge TSV files by taxonomic annotations.")
    parser.add_argument('files', nargs='+', help='Paths to the TSV files')
    parser.add_argument('-o', '--output', help='Output tsv file name', default='merged_data.tsv')
    parser.add_argument('--column', choices=['relative_abundance', 'sequence_abundance', 'ANI'], required=True,
                        help='The data column to merge')
    args = parser.parse_args()

    merged_df = merge_data(args.files, args.column)
    output_file = args.output
    merged_df.to_csv(output_file, sep='\t')
    print(f"Merged data written to {output_file}")

if __name__ == "__main__":
    main()
