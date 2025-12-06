#!/bin/bash

# Define the directory (current directory by default)
DIR="."

# Loop through all .txt files in the directory
for file in "$DIR"/*stg5.log; do
    # Check if there are any matching files
    [ -e "$file" ] || continue

    # Read and print lines that start with " Error Report for " along with the file name
    grep -i 'Error Report for' $file
    #grep -i 'Loading lookup table from' $file 
    echo $file

done
