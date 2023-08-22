#  Generating Multiple Sequence Alignment (MSA) for EVE software

## Description
The script generates an MSA for the proteins of interest contained
in the `.csv` . This MSA then can be used for the EVE software.

## Requirements

### Software

  - [EVcouplings](https://github.com/debbiemarkslab/EVcouplings)
  - [HMMER](http://hmmer.org/download.html)

Please follow their respective websites for installation instructions.
For our purposes, we installed them in a custom Python environment using
`virtualenv`.

### Databases

  - UniRef100, as available on [UniProt](https://www.uniprot.org/help/downloads)

We have used UniRef100 - using other UniRef databases is also possible.

## Installation

No installation is required - just clone this repository to a local folder,
provide the required input files (see below) and run the included script. 

## Usage

### Input files 

  - one `.csv` file (see below)
  - one `config.yaml` configuration file

The `.csv` file to be used must have a format similar to:

```
prefix,uniprotIDS
SMPD1,P17405
VCP,P55072
NPLOC4,Q8TAT6
...
```

The `prefix` column contains names chosen by the user to refer to a 
specific protein (here we are using the corresponding gene name). This will also
be the name assigned to the output folder in which the respective alignment will be stored.

The `uniprotIDS` column represents the UniProt AC or ID of the protein.

The `config.yaml` is a config file for the `EVcouplings` software, as available 
[on their GitHub](https://github.com/debbiemarkslab/EVcouplings)
Here we include a customized version of the original file.

**Important**: users must specify 
  - the installation path of the HHMER binaries 
  - the databases of sequences to use and their location
in the configuration file

```
bash MSA_generator.bash config.yaml  *.csv  Ncore
```

Where `Ncore` is the number of core to use and `*.csv` is the file that the user prepared ( or downloaded). 
 

### Example Run 
```
bash MSA_generator.bash config.yaml uniprotIDS.csv 4
```

## Output
The output consists in one folder for each line of the input `.csv` file, named 
after the content of the `prefix` column. Each folder contains the respective
output alignment.