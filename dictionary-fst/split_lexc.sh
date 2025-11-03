#!/bin/bash


file="dict.lexc"


# Get total number of lines
total_lines=$(wc -l < "$file")

# Compute the midpoint (integer division)
half_lines=$((total_lines / 2))

# Generate output filenames
base="${file%.*}"
ext="${file##*.}"

# Handle case where file has no extension
if [ "$base" = "$file" ]; then
    part1="${file}_part1"
    part2="${file}_part2"
else
    part1="${base}1.${ext}"
    part2="${base}2.${ext}"
fi

# Split the file
head -n "$half_lines" "$file" > "$part1"
tail -n +"$((half_lines + 1))" "$file" > "$part2"

echo "File successfully split into:"
echo "  $part1"
echo "  $part2"