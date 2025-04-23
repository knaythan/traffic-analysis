#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <dataset_file.csv> <number_of_splits>"
    exit 1
fi

dataset_file=$1
num_splits=$2

# Check if the dataset file exists
if [ ! -f "$dataset_file" ]; then
    echo "Error: File '$dataset_file' not found!"
    exit 1
fi

# Ensure the file has a .csv extension
if [[ "${dataset_file##*.}" != "csv" ]]; then
    echo "Error: Input file must be a .csv file!"
    exit 1
fi

# Get the directory of the dataset file
output_dir=$(dirname "$dataset_file")

# Get the total number of lines in the dataset
total_lines=$(wc -l < "$dataset_file")

# Calculate the number of lines per split
lines_per_split=$(( (total_lines + num_splits - 1) / num_splits ))

# Split the dataset into chunks
split -l "$lines_per_split" -d --additional-suffix=".csv" "$dataset_file" "$output_dir/${dataset_file%.*}_part"

# Rename the split files to have _01, _02, etc. suffixes
counter=1
for file in "$output_dir/${dataset_file%.*}_part"*.csv; do
    new_name="$output_dir/${dataset_file%.*}_$(printf "%02d" $counter).csv"
    mv "$file" "$new_name"
    counter=$((counter + 1))
done

echo "Dataset split into $num_splits parts in directory: $output_dir."