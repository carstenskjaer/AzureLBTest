import socket
import sys
import time
import struct

hostname = socket.gethostname()

def recv_bytes(s, bytecount):
    buf = bytearray(bytecount)
    view = memoryview(buf)
    while bytecount:
        nbytes = s.recv_into(view, bytecount)
        view = view[nbytes:] # slicing views is cheap
        bytecount -= nbytes
    return buf

def client_connect(sock, server_address):
    print(f'Client on {hostname} connecting to {server_address}')
    while(True):
        try:
            sock.connect(server_address)
            return
        except socket.error as e:
            print(f'exception {e} when trying to connect')
            time.sleep(0.1)


def client(server):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) # Timeout to 1 s

    # Connect the socket to the port where the server is listening
    server_address = (server, 10000)
    client_connect(sock, server_address)

    iterations = 10000000

    totalStartTime = time.time()

    for i in range(iterations):
        try:
            # Send data
            payloadSize = 512**2
            request = struct.pack('4s2i', bytes('abcd', 'ascii'), 0, payloadSize)
            request += bytearray(payloadSize)
            startTime = time.time()
            sock.sendall(request)

            # Receive response
            replyHeaderStruct = struct.Struct('4ci64si')

            data = recv_bytes(sock, replyHeaderStruct.size)
            header = replyHeaderStruct.unpack(data)

            if (header[0] != b'e' or header[1] != b'f' or header[2] != b'g' or header[3] != b'h'):
                raise socket.error(f'Invalid header {header[0:3]}')

            status = header[4]
            hostname = (header[5]).decode('ascii')
            payloadSize = header[6]

            payload = recv_bytes(sock, payloadSize)

            print(f'send+recv to {hostname} took  {(time.time() - startTime)*1000.0*1000.0:.2f}us')
        except socket.error as e:
            print(f'exception {e}')
            print('closing and reopening socket')
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_connect(sock, server_address)
        except:
            print(f'unknown exception')
            raise
    sock.close()

    duration = (time.time() - totalStartTime)
    print(f'{iterations} iterations took {duration*1000.0*1000.0:.2f}us for an avg {(duration/iterations)*1000.0*1000.0:.2f}us')


def server():
    hostname = socket.gethostname()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('', 10000)
    print(f'Running server on {hostname} - binding to {server_address}')
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
                response = struct.pack('4si64si', bytes('efgh', 'ascii'), 0, bytes(hostname, 'ascii'), payloadSize)
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

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        client(sys.argv[1])
    else:
        server()
