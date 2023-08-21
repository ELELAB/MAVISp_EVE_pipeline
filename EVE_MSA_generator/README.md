#  Generating Multiple Sequence Alignment (MSA) for EVE software
## Description
The script generates an MSA for the proteins of interest contained
in the `.csv` . This MSA then can be used for the EVE software.

## Requirements

### Input files 
```
*.csv 
config.yaml
```

The `.csv` file to be used must be formatted be in the following way:

```
prefix,uniprotIDS
SMPD1,P17405
VCP,P55072
NPLOC4,Q8TAT6
```

Where the `prefix` column is a name chosen by the user to refer to the protein. This will also be
the name assigned to the output folder in which the respective alignment will be stored.
On the other hand the `uniprotIDS` column represents the uniprot ID of the protein.

The `config.yaml` is a config file originally developed for the EVcoupling software.
Here we provided a custom version of the original file. The original file can be found at the software github page ( listed below).

**N.B**
In the config file the user must specify the path where the HHMER tools are installed and the databases of sequences to use;  i.e Uniprot, Uniref90  or Uniref100. To our purpose we are using Uniref100.

### Softwares
```
EVcoupling 
HMMER 
``` 

These can be found at https://github.com/debbiemarkslab/EVcouplings and http://hmmer.org/download.html . 
To our purposes we created a custom python environment using virtualenv tool.

### Databases
```
Uniref100
```

This depends on the user need. Only download the ones you want to use. To our purpose we are using Uniref100, it can be found here: https://www.uniprot.org/help/downloads


## Usage
```
bash MSA_generator.bash config.yaml  *.csv  Ncore
```

Where `Ncore` is the number of core to use and `*.csv` is the file that the user prepared ( or downloaded). 
 

### Example Run 
```
bash MSA_generator.bash config.yaml uniprotIDS.csv 4
```

## Output
The output consists in a folder named (for each protein) after the `prefix` specified in the .csv file, containing the alignment for that protein.
