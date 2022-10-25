import socket

try:
    sock = socket.socket()
    sock.setblocking(1)
    print('Input address, port:', end=' ')
    default = input()
    if default == 'local':
        default = ('localhost', 9090)
    else:
        default = default.split(' ')
        default[1] = int(default[1])
    sock.connect(tuple(default))
    print("Connect to server")

    msg = input()
    sock.send(msg.encode())
    print("Data sending...")

    data = sock.recv(1024)
    print("Done")
except KeyboardInterrupt:
    sock.send("Client disconnect".encode())

sock.close()

print("Data receiving...")
print(data.decode())