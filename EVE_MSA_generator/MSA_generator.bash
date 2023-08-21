#!/usr/bin/bash

# Source environment 
source /usr/local/envs/eve/eve/bin/activate

# Check if input arguments are provided
if [ $# -ne 3 ]; then
  echo "Usage: $0 <config.yaml> <uniprot.csv> <Ncore>"
  exit 1
fi

# Set input arguments
config=$1
csv=$2
core=$3

# Define function to update config file  
update_config() {
  sed -i "s/$1:.*/$1: $2/" ${config}
}

# Read CSV file and run evcouplings_runcfg for each uniprot ID in the .csv file
tail -n +2 "${csv}" | while IFS="," read -r prefix uniprotID; 
do
    update_config "prefix" "${prefix}"
    update_config "sequence_id" "${uniprotID}"
    update_config "cpu" "${core}"
    evcouplings_runcfg ${config}
done

# Reset config
update_config "prefix" ""
update_config "sequence_id" ""
update_config "cpu" ""

# Clean up
rm -f *.done *.fasta *.outcfg