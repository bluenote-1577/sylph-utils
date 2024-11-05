#### CHANGELOG

_2024-11-05 - version 0.4_

Adding releases now. 

* Renamed `fungi` to `eukaryote`.
* Added `eukaryote/tara_SMAGs_metadata.tsv.gz` for the TARA eukaryoatic SMAGs. 

_2024-10-03 - version 0.3_

`sylph_to_taxprof.py`:

* The script now fails if it detects ambiguous sample names
* Added the `-f` or `--add-folder-information` flag to include directory information into the output `.sylphmpa` files; this can disambiguate sample names.

_2024-07-25 - version 0.2_

* Added IMG/VR 4.1 taxonomy and fungi refseq taxonomy.
* Added coverage information into the `.sylphmpa` files
* Added capabilities to do viral-host annotation if the IMG/VR 4.1 metadata is used. 
