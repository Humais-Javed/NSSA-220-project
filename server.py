import socket
import csv
import time
import xml.etree.ElementTree as ET


def execute(query_str):
    # Assuming your data is stored in a variable called 'data'
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Parse the incoming query
    tree = ET.fromstring(query_str)
    query_type = tree.find("type").text
    columns = [column.text for column in tree.findall(".//columns/column")]
    conditions = {condition.find("column").text: condition.find("value").text
                  for condition in tree.findall(".//conditions")}

    # Determine the requested column dynamically
    requested_column = columns[0]  # Assuming the first column in the query
    if requested_column not in data[0]:  # Check if the column exists in the data
        raise ValueError(f"Requested column '{requested_column}' not found in the data")

    # Apply conditions
    print("Applying conditions:", conditions)
    filtered_data = [row for row in data if all(row[column] == value for column, value in conditions.items())]

    # Prepare CSV response
    csv_response = f"{requested_column}\n"
    for row in filtered_data:
        csv_response += f"{row[requested_column]}\n"

    return csv_response

def handle_client(client_socket):
    try:
        while True:
            query = client_socket.recv(1024)
            if not query:
                break
            query_str = query.decode("utf-8")
            if query_str == "exit":
                print("Client requested exit. Closing connection.")
                break
            print("Received query:", query_str)
            response = execute(query_str)

            # Send the response in chunks to ensure complete transmission
            chunk_size = 1024
            for i in range(0, len(response), chunk_size):
                client_socket.send(response[i:i + chunk_size].encode("utf-8"))

            # Add a small delay to allow the client to process each chunk
            time.sleep(0.1)

        print("Closing connection.")
    except ConnectionResetError:
        print("Connection reset by client.")
    finally:
        # Do not close the client socket here to keep the server open for new connections
        pass
    
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)

    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from", addr)
        handle_client(client_socket)

if __name__ == "__main__":
    main()

