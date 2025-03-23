#!/bin/bash

# Check if the user provided an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <new_path>"
    exit 1
fi

NEW_PATH="$1"

# Iterate through all text files in the current directory
for file in *.txt; do
    if [ -f "$file" ]; then
        sed -i "s|/yourPath|$NEW_PATH|g" "$file"
        echo "Updated: $file"
    fi
done

echo "Replaced the path in all the files."
