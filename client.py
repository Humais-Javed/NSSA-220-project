import sys 
import socket
import xml.etree.ElementTree as ET
import time

def parse_xml_query(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    query = ET.tostring(root, encoding='unicode', method='xml')
    return query

def main():
    host = "localhost"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    query_file = sys.argv[1] if len(sys.argv) > 1 else "query1.xml"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output1.csv"

    query = parse_xml_query(query_file)
    client_socket.send(query.encode("utf-8"))

    # Receive the response in chunks and concatenate them
    response_str = ""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        response_str += chunk.decode("utf-8")
        print(chunk.decode("utf-8"), end='')  # Print received data to the terminal

    print("\nReceived response:", response_str)

    # Print debugging information about file handling
    print("Output file:", output_file)
    try:
        with open(output_file, "w") as f:
            f.write(response_str)
        print("Write successful")
    except Exception as e:
        print("Error writing to output file:", e)

    client_socket.close()

if __name__ == "__main__":
    main()
