import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('', 10000)
print(f'binding to {server_address}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        connectTime = time.time()
        print(f'connection from {client_address}')

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16*1024)
            print(f'\treceived data of size {len(data)}')
            if data:
                connection.sendall(data)
            else:
                print(f'\tno more data from {client_address}')
                break
            
    finally:
        # Clean up the connection
        connection.close()
        print(f'closed after {(time.time() - connectTime)*1000.0*1000.0:.2f}us')
