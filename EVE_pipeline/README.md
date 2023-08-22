#  Snakemake pipeline for Evolutionary model of Variant Effects (EVE)

## Description

This is a customizable snakemake pipeline for computing EVE scores for a protein.
It is based on the available scripts for running EVE, described on the original
[EVE GitHub](https://github.com/OATML/EVE).

If you use this code, please cite the original EVE paper, as well as the original
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

### example_mapping.csv

The `example_mapping.csv` file needs to be modified with information on the protein(s)
of interest and has the following format:

```
protein_name,msa_location,theta
NALP7_HUMAN,NALP7_HUMAN_b03.a2m,0.2 
```

The first field specifies the name of the protein of interest, the second
specifies the name of the alignment file and the theta is the "Sequence weighting hyperparameter" for EVE.
The name `example_mapping.csv` was kept as a default from the original EVE workflow.
However, it can be renamed by the user.


#### config.yaml

The `config.yaml` contains all the customizable options of the pipeline:

```
mpi:
    Ncore: 8
paths:
    source: 
        activate: 'set +u; source /usr/local/envs/eve/eve/bin/activate ; set -u'
    inputs: 
        Step1:
            clinvar_file : '/data/user/shared_projects/mavisp/ADCK1/downstream_analysis/mavisp_csv/15062023/ADCK1-simple_mode.csv'
            MSA_data_folder: '/data/databases/EVE/local_MSA/ADCK1/align' 
            MSA_list: 'example_mapping.csv'
```

In particular:

  - `Ncore` specifies the number of cores to be used
  - `clinvar_file` specify the path of the final `.csv` aggregated file from the MAVISp workflow
  - `MSA_data_folder` is the path of the folder containing the multiple sequence alignments
  for EVE. The name of the alignment is specified in `example_mapping.csv`, in the second columns (see above)
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
The pipeline will automatically generate a `data/` folder in which subfolders and files will be created depending
on workflow step. An example following the `example_mapping.csv` above: 

```
data/
|----- Step1/  
        |----- weights/
        NALP7_HUMAN_theta_0.2.npy
|----- Step2/
        |----- mutations/
        NALP7_HUMAN_all_singles.csv
|----- Step3
        |-----GMM_parameters
               |----- 12082023
                       GMM_model_dictionary_12082023  
                       GMM_pathogenic_cluster_index_dictionary_12082023  
                       GMM_stats_12082023.csv
        |----- labels/
               ClinVar_labels.csv
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

The final output files can be found in the folder `results` inside `data/`.
The `.csv` file within `EVE_scores` contains all the EVE scores for out protein.
On the other hand, EVE will generate automatically the `plots_scores_vs_labels` 
and `plots_histograms` containing useful plots in PNG format.