import socket
import sys
import time
import struct

def recv_bytes(s, bytecount):
    buf = bytearray(bytecount)
    view = memoryview(buf)
    while bytecount:
        nbytes = s.recv_into(view, bytecount)
        view = view[nbytes:] # slicing views is cheap
        bytecount -= nbytes
    return buf

hostName = socket.gethostname()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10000)
print(f'Running on {hostName} - binding to {server_address}')
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

        requestHeaderStruct = struct.Struct('4c2i')

        while True:
            # Receive request
            data = connection.recv(requestHeaderStruct.size)
            header = requestHeaderStruct.unpack(data)
            if (header[0] != b'a' or header[1] != b'b' or header[2] != b'c' or header[3] != b'd'):
                raise Exception(f'Invalid header {header[0:4]}')
            command = header[4]
            payloadSize = header[5]
            payload = recv_bytes(connection, payloadSize)

            # Send response
            response = struct.pack('4si64si', bytes('efgh', 'ascii'), 0, bytes(hostName, 'ascii'), payloadSize)
            response += payload
            connection.sendall(response)

            print(f'\tReceived request with command {command} and payload of size {payloadSize} and returned response')
    except socket.error as err:
        print(f'exception {err}')
    except Exception as err:
        print(f'exception {err}')
    except:
        print(f'unknown exception')
    finally:
        # Clean up the connection
        connection.close()
        print(f'closed after {(time.time() - connectTime)*1000.0*1000.0:.2f}us')



