# sylph-utils: utility scripts for [sylph](https://github.com/bluenote-1577/sylph)

This repository contains helper scripts for manipulating the output of [sylph](https://github.com/bluenote-1577/sylph). 

### sylph_to_taxprof.py - obtaining taxonomic profiles

Turn sylph's tsv output into a taxonomic profile.  

```sh
python sylph_to_taxprof.py -m database_metadata.tsv.gz -s sylph_output.tsv -o prefix_or_folder/
```
* `-m`: taxonomy metadata file. Metadata files are present in this repository.
* `-s`: the output from sylph. The database used has to coincide with the `-m` option. 
* `-o`: prepends this prefix to all of the output files; one output for each sample in the sylph output. 

You have to use the metadata file corresponding to the database used. So if you use the GTDB-R214 database for sylph, you have to use the `gtdb_r214_metadata.tsv.gz` file. 

See [here](https://github.com/bluenote-1577/sylph/wiki/Integrating-taxonomic-information-with-sylph#custom-taxonomies-and-how-it-works) for more information on how these taxonomy metadata files are defined and the resulting output.

The following databases are currently supported 
(with pre-built sylph databases [available here](https://github.com/bluenote-1577/sylph/wiki/Pre%E2%80%90built-databases):

1. [GTDB-R214](https://gtdb.ecogenomic.org/)  
2. [OceanDNA](https://doi.org/10.1038/s41597-022-01392-5)
3. [SMAG](https://www.nature.com/articles/s41467-023-43000-z)
