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

        print(f'send+recv took  {(time.time() - startTime)*1000.0*1000.0:.2f}us')
    except socket.error as e:
        print(f'exception {e}')
        print('closing and reopening socket')
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
    except:
        print(f'unknown exception')
        raise
sock.close()

duration = (time.time() - totalStartTime)
print(f'{iterations} iterations took {duration*1000.0*1000.0:.2f}us for an avg {(duration/iterations)*1000.0*1000.0:.2f}us')


