#  Snakemake pipeline for Evolutionary model of Variant Effects (EVE)
## Description
Customizable snakemake pipeline for computing EVE scores for a protein.
EVE can be found here : https://github.com/OATML-Markslab/EVE. 

## Requirements

### Input files 

```
data/
Snakefile
config.yaml
```

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

The `example_mapping.csv` needs to be modified depending on
the protein of interest and is formatted in the following way :
```
protein_name,msa_location,theta
NALP7_HUMAN,NALP7_HUMAN_b03.a2m,0.2 
``` 
The first field specify the name we want to assign to our protein, the second
specify the alignment file and the theta is the "Sequence weighting hyperparameter".
The user can generate the file on its own, but will need to also modify the config file 
accordingly.


The `PTEN_ClinVar_labels.csv` contains the reference labels from ClinVar and 
is formatted in the following way:
```
protein_name,mutations,ClinVar_labels
1433G_HUMAN,D99N,0.0
1433G_HUMAN,D129E,1.0
```

Where `0.0` represents the mutation being benign and `1.0` pathogenic.

The `config.yaml` contains all the customizable options of the pipeline such as:
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

The file is already provided in the `data/` folder. 

N.B 
The number of core should be the same when running snakemake from command line and the config
file.  

### Softwares
```
EVE
Snakemake 
``` 

EVE github can be found at https://github.com/OATML-Markslab/EVE. In our case we created a
a virtual environment named `eve`.
Snakemake guidelines for installation are available here:
https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

### Databases

EVE authors made available a databases of alignment. It can be found here:
https://evemodel.org/. 
In this database not all  proteins are available. In such case the user needs
to generate the alignment for the protein of interest.
To do so we developed an easy pipeline that can be found here : 
https://github.com/ELELAB/CSB-scripts/tree/master/CSB-SB/EVE_MSA_generator.



## Usage
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
On the other hand, EVE will generate automatically the `plots_scores_vs_labels` and `plots_histograms` containing all the plots in `.png` format. 

# N.B
The size of the protein alignment will have an impact on the performance of EVE prior to the training step. It may take some time before initiating the protocol itself.
