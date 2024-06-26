# sylph-utils: utility scripts and taxonomy for [sylph](https://github.com/bluenote-1577/sylph)

This repository contains helper scripts for manipulating the output of [sylph](https://github.com/bluenote-1577/sylph). 

### Taxonomy integration - available databases 
The following databases are currently supported (with pre-built sylph databases [available here](https://github.com/bluenote-1577/sylph/wiki/Pre%E2%80%90built-databases)):

1. [GTDB-R220 (April 2024)](https://gtdb.ecogenomic.org/stats/r220) - `gtdb_r220_metadata.tsv.gz`
1. [GTDB-R214 (April 2023)](https://gtdb.ecogenomic.org/stats/r214) - `gtdb_r214_metadata.tsv.gz`
2. [OceanDNA](https://doi.org/10.1038/s41597-022-01392-5) - `ocean_dna_metadata.tsv.gz`
3. [SMAG](https://www.nature.com/articles/s41467-023-43000-z) - `smag_metadata.tsv.gz`



### Requirements/Install

* Python3
* Pandas

Run `pip install pandas` if pandas is not installed. 

## sylph_to_taxprof.py - obtaining taxonomic profiles from sylph's output

```sh
python sylph_to_taxprof.py -m database_metadata.tsv.gz -s sylph_output.tsv -o prefix_or_folder/
```
* `-m`: taxonomy metadata file. Metadata files are present in this repository.
* `-s`: the output from sylph. Sylph's database must be the same as the `-m` option's.
* `-o`: prepends this prefix to all of the output files; one output for each sample in the sylph output.
* Output suffix is `.sylphmpa`.  

Use the metadata file corresponding to the database used. E.g. if you use the GTDB-R220 database for sylph, you **must** use the `gtdb_r220_metadata.tsv.gz` file. 

See [here](https://github.com/bluenote-1577/sylph/wiki/Integrating-taxonomic-information-with-sylph#custom-taxonomies-and-how-it-works) for more information on 

1. taxonomy metadata files definitions
2. the output format
3. how to create taxonomy metadata for customized genome databases

Hint: in python, you can read outputs with `pd.read_csv('output.sylphmpa',sep='\t', comment='#')`.

#### CHANGELOG

_2024-03-19 - version 0.1_ 
* Changed the format slightly. Removed the # in front of the header. 
  
## merge_sylph_taxprof.py - merge multiple taxonomic profiles

Merge multiple taxonomic profiles from `sylph_to_taxprof.py` into a TSV table 

```sh
python merge_sylph_taxprof.py *.sylphmpa --column {ANI, relative_abundance, sequence_abundance} -o output_table.tsv
```

* `*.sylphmpa` files from sylph_to_taxprof.py. 
* `--column` can be ANI, relative abundance, or sequence abundance (see paper for difference between abundances)
* `-o` output file in TSV format.

#### Output format
```sh
clade_name  sample1.fastq.gz  sample2.fastq.gz
d__Archaea  0.0  1.1
d__Archaea|p__Methanobacteriota 0.0     0.0965
...
```
