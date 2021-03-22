import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], 10000)
print(f'connecting to {server_address}')
sock.connect(server_address)

iterations = 10

totalStartTime = time.time()

for i in range(iterations):
    try:
        # Send data
        message = b'This is the message.  It will be repeated.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        print(f'sending data of size {len(message)}')
        startTime = time.time()
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16*1024)
            amount_received += len(data)
            print(f'received {len(data)} bytes')

        print(f'send+recv took  {(time.time() - startTime)*1000.0*1000.0:.2f}us')

    except socket.error as e:
        print(f'exception {e}')
        print('closing and reopening socket')
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)


sock.close()

duration = (time.time() - totalStartTime)
print(f'{iterations} iterations took {duration*1000.0*1000.0:.2f}us for an avg {(duration/iterations)*1000.0*1000.0:.2f}us')


