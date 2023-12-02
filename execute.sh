#!/bin/bash

# Check if both XML and CSV file paths are provided as arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <XML_INPUT_FILE> <CSV_OUTPUT_FILE>"
    exit 1
fi

# Assign provided arguments to variables
CLIENT_QUERY_FILE="$1"
OUTPUT_CSV_FILE="$2"

SERVER_PY_PATH="/Users/muhammadhumaisjaved/Desktop/NSSA/server/server.py"

# Start the server in a separate terminal
osascript -e 'tell app "Terminal" to do script "cd /Users/muhammadhumaisjaved/Desktop/NSSA/server && python3 server.py"'

# Sleep to ensure the server has started before the client tries to connect
sleep 2

# Run the client in a separate terminal with provided arguments
osascript -e "tell app \"Terminal\" to do script \"cd /Users/muhammadhumaisjaved/Desktop/NSSA/client && python3 client.py $CLIENT_QUERY_FILE $OUTPUT_CSV_FILE\""
