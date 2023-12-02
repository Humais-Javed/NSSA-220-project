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

    query_file = sys.argv[1] if len(sys.argv) > 1 else "client/query6.xml"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "client/output6.csv"

    query = parse_xml_query(query_file)
    client_socket.send(query.encode("utf-8"))

    # Add a delay here (you can adjust the duration based on your server's processing time)
    time.sleep(6)

    response = client_socket.recv(1024)
    response_str = response.decode("utf-8")
    print("Received response:", response_str)

    with open(output_file, "w") as f:
        f.write(response_str)

if __name__ == "__main__":
    main()
