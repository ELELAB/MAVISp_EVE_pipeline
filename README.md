Cancer Systems Biology, Technical University of Denmark, 2800, Lyngby, Denmark Cancer Structural Biology, Danish Cancer Society Research Center, 2100, Copenhagen, Denmark
Cancer Structural Biology, Danish Cancer Institute, 2100, Copenhagen, Denmark

# MAVISp EVE workflow

This repository containing the Evolutionary model of Variant Effects (EVE) 
workflow for [the MAVISp project](https://github.com/ELELAB/MAVISp). It is made
of two computational pipelines: one for the generation of the multiple sequence
alignment, which is necessary to run EVE, and one for the calculation of the EVE
scores themselves.

It should be noted that this is just a convenient restructuring of the 
steps that are necessary to run EVE, and not an reimplementation of the algorithm
itself. It expects the original EVE implementation to be installed and it is 
derived from the instructions and scripts available on the [EVE GitHub](https://github.com/OATML/EVE).

The project is a joint collaboration between Marks lab (https://www.deboramarkslab.com/) 
and the OATML group (https://oatml.cs.ox.ac.uk/). 
It is available at :https://github.com/OATML-Markslab/EVE or at the webserver: https://evemodel.org/ .

If you use this code, please follow the [citation guidelines on the EVE original 
GitHub](https://github.com/OATML/EVE) to properly cite EVE. Currently, this means 
citing the main EVE publication:

```https://www.nature.com/articles/s41586-021-04043-8```

Please also cite the original MAVISp paper:

```...```
 
EVE serves as a model designed to predict the clinical relevance of 
human genetic variants by leveraging evolutionary sequence information 
from a range of diverse organisms. The full workflow is made of two different steps:

## Step 1 : Multiple Sequence Alignment Generation 
This step generates a MSA for the proteins of interest that is used by the EVE software in Step 2.
The folder *EVE_MSA_generator* contains all the required resources and documentation. 

## Step 2: Automated Snakemake pipeline
This step employs a snakemake pipeline for computing the EVE scores for a protein of interest. 
The folder *EVE_pipeline* contains all the required resources and documentation.

## Documentation
For the specifics of Step 1 and Step 2, installation instructions, usage guidelines,
licensing information we refer to files available in each specific folder.