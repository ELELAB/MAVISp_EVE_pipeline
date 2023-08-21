# MAVISp EVE workflow

Repository containing the Evolutionary model of Variant Effects (EVE) 
workflow for MAVISp project.
EVE serves as a model designed to predict the clinical relevance of 
human genetic variants by leveraging evolutionary sequence information 
from a range of diverse organisms.
The workflow is divided in two different steps.

## Step 1 : Multiple Sequence Alignment Generation 
This step generates a MSA for the proteins of interest that is used by the EVE software in Step 2.
The folder *EVE_MSA_generator* contains all the required resources and documentation. 


## Step 2: Automated Snakemake pipeline
This step employs a snakemake pipeline for computing the EVE scores for a protein of interest. 
The folder *EVE_pipeline* contains all the required resources and documentation.

**N.B** <br>
For the specifics of Step 1 and Step 2, installation instructions, usage guidelines etc... we refer to 
the README in the folder.