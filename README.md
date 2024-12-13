# sylph-utils: utility scripts and taxonomy for [sylph](https://github.com/bluenote-1577/sylph)

This repository contains scripts for incorporating taxonomic information into the output of [sylph](https://github.com/bluenote-1577/sylph). 

> [!WARNING]
> sylph-utils is now replaced with [sylph-tax](https://github.com/bluenote-1577/sylph-tax). Sylph-tax offers a cleaner interface. Sylph-utils still works as of sylph v0.8 but will no longer be updated. 

### Taxonomy integration - available databases 
The following databases are currently supported (with pre-built sylph databases [available here](https://github.com/bluenote-1577/sylph/wiki/Pre%E2%80%90built-databases)) and can be found in the `prokaryote, eukaryote, virus` subfolders within this repository. 

1. [GTDB-R220 (April 2024)](https://gtdb.ecogenomic.org/stats/r220) - `prokaryote/gtdb_r220_metadata.tsv.gz`
2. [GTDB-R214 (April 2023)](https://gtdb.ecogenomic.org/stats/r214) - `prokaryote/gtdb_r214_metadata.tsv.gz`
3. [OceanDNA](https://doi.org/10.1038/s41597-022-01392-5) - `prokaryote/ocean_dna_metadata.tsv.gz`
4. [Soil MAGs (SMAG) from Ma et al.](https://www.nature.com/articles/s41467-023-43000-z) - `prokaryote/smag_metadata.tsv.gz`
5. Refseq fungi representative genomes - `eukaryote/fungi_refseq_2024-07-25_metadata.tsv.gz`
6. [TARA eukaryotic SMAGs](https://www.sciencedirect.com/science/article/pii/S2666979X22000477) - `eukaryote/tara_SMAGs_metadata.tsv.gz`
7. [IMG/VR 4.1 high-confidence viral OTU genomes](https://genome.jgi.doe.gov/portal/IMG_VR/IMG_VR.home.html) - `virus/IMGVR_4.1_metadata.tsv.gz`

> [!IMPORTANT]
> **(2024-11-05)**: `fungi` directory renamed -> `eukaryote`. TARA eukaryote taxonomy now available. See CHANGELOG.md for details. 

### Requirements/Install

* Python3
* Pandas

Run `pip install pandas` if pandas is not installed. 

## sylph_to_taxprof.py - obtaining taxonomic profiles from sylph's output

```sh
python sylph_to_taxprof.py -m database1_metadata.tsv.gz database2_metadata.tsv.gz -s sylph_output.tsv -o prefix_or_folder/
```
* `-m`: taxonomy metadata file(s). Multiple taxonomy metadata files can be input (will be concatenated). Metadata files are of the form `tsv.gz` and present in this repository. (e.g. `prokaryote/gtdb_r220_metadata.tsv.gz`)
* `-s`: the output from sylph. Sylph's databases must be the same as the `-m` option's.
* `-o`: prepends this prefix to all of the output files; one output for each sample in the sylph output.
* `--annotate-virus-hosts` (new in v0.2): annotates found viral genomes with host information metadata (only available for IMG/VR 4.1 right now) 
* Output suffix is `.sylphmpa`.  

Use the metadata file corresponding to the database used. E.g. if you use the GTDB-R220 database for sylph, you **must** use the `gtdb_r220_metadata.tsv.gz` file. 

See [here](https://github.com/bluenote-1577/sylph/wiki/Integrating-taxonomic-information-with-sylph#custom-taxonomies-and-how-it-works) for more information on 

1. taxonomy metadata files definitions
2. the output format
3. how to create taxonomy metadata for customized genome databases

> [!TIP]
> In python/pandas, you can read the output with `pd.read_csv('output.sylphmpa',sep='\t', comment='#')`.

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
