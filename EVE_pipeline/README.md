#  Snakemake pipeline for Evolutionary model of Variant Effects (EVE)

## Description

This is a customizable snakemake pipeline for computing EVE scores for a protein.
It is based on the available scripts for running EVE, described on the original
[EVE GitHub](https://github.com/OATML/EVE).

If you use thie code, please cite the original EVE paper, as well as the original
MAVISp paper, as stated in the README file in the main folder of this repository.

## Requirements

### Software

This pipeline requires:
  
  - Python >=3.8
  - [the EVE scripts](https://github.com/OATML-Markslab/EVE) and their requirements
  - a few other Python packages:
       - [Snakemake](https://snakemake.readthedocs.io/en/stable/)
       - [pandas](https://pandas.pydata.org)
       - [numpy](https://numpy.org)

Please refer to the respective websites for installation instructions. In our
case, we have installed all the requirements in a dedicated Python virtual environment.

## Installation

No installation is required - just clone this repository to a local folder,
provide the required input files (see below) and run Snakemake as described below. 

## Usage

### Input files 

#### `data` folder

The `data/` folder is divided in multiple subfolders containing different
mandatory input files and folders where the output will be stored.

```
data/
|----- Step1/  
        |----- mapping/
               example_mapping.csv
        |----- weights/
|----- Step2/
        |----- mutations/
|----- Step3
        |----- labels/
               PTEN_ClinVar_labels.csv
|----- results
        |----- EVE_scores  
        |----- VAE_parameters  
        |----- logs
        |----- evol_indices
```

The `example_mapping.csv` file needs to be modified with information on the protein(s)
of interest and has the following format:

protein_name,msa_location,theta
NALP7_HUMAN,NALP7_HUMAN_b03.a2m,0.2 
```

The first field specifies the name of our protein, the second
specifies the name of the alignment file and the theta is the
"Sequence weighting hyperparameter" for EVE.

The `PTEN_ClinVar_labels.csv` contains the reference labels from ClinVar and 
has the following format:

```
protein_name,mutations,ClinVar_labels
1433G_HUMAN,D99N,0.0
1433G_HUMAN,D129E,1.0
```

Where the first column is the protein name as specified in the `example_mapping.csv`
and where `0.0` represents its reference classification in Clinvar, with 0.0 as benign
and `1.0` as pathogenic.

#### config.yaml

The `config.yaml` contains all the customizable options of the pipeline:

```
mpi:
    Ncore: 8 
paths:
    source: 
        activate: 'set +u; source /usr/local/envs/eve/eve/bin/activate ; set -u'
    inputs: 
        MSA_data_folder: '/data/databases/EVE/08112021/MSAs/' 
        MSA_list: 'data/Step1/mapping/example_mapping.csv'
```

In particular:

  - `Ncore` specifies the number of cores to be used
  - `MSA_data_folder` is the folder containing the multiple sequence alignments
  for EVE. These should be named ...
  - `MSA_list` should point to the `example_mapping.csv` file described above

Notice that the specified number of cores should be the same when running
snakemake from command line and the config file.

### Running the pipeline

Just run:

```
snakemake --configfile config.yaml -c 8
```

Where `cores` is the number of core to use and `config.yaml` is the config file. 
 
## Output
The output files can be found in the folder `results` in `data/`.
The final output folders should look like this:

```
|----- results
        |----- EVE_scores
               *.csv 
        |----- VAE_parameters  
               *_final
        |----- logs
        |----- evol_indices
               *.csv
        |----- plots_scores_vs_labels
                    |----- snakemake_example
                           *.png
        |----- plots_histograms
                    |----- snakemake_example
                           *.png
                           *.png
``` 

The `.csv` file within `EVE_scores` contains all the EVE scores for out protein.
On the other hand, EVE will generate automatically the `plots_scores_vs_labels` 
and `plots_histograms` containing useful plots in PNG format.