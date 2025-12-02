#!/bin/bash

# Thank you for this file gemini

# The name of the file to upload.
# You can change this to any file you like.
FILE_NAME="Cargo.toml"

# Create a dummy file to upload if it doesn't exist
if [ ! -f "$FILE_NAME" ]; then
    echo "Creating dummy file: $FILE_NAME"
    touch "$FILE_NAME"
fi

# Send the request to the server
curl -F "file=@$FILE_NAME" \
     -F "json={\"name\":\"$FILE_NAME\"};type=application/json" \
     http://127.0.0.1:8080/file

echo "\n"
