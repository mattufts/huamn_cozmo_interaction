#!/bin/bash

# Loop over all files that match the pattern in the current directory
for file in *menthol-3D-qutemol.anim-*.png; do
    # Extract the sequence number from the original file name using parameter expansion
    seq_number="${file##*-}"
    seq_number="${seq_number%.png}"
    
    # Format the new file name with zero-padding for the sequence number
    new_file_name=$(printf "PNG_%04d.png" "$seq_number")
    
    # Rename the file
    mv "$file" "$new_file_name"
    
    # Optional: print out what was renamed for verification
    echo "Renamed $file to $new_file_name"
done
