import socket
from select import select

HOST = ('localhost', 5000)
to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(HOST)
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Got connection from', addr)
    to_monitor.append(client_socket)


def send_message(client_socket):
    print('Before recv')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], []) # read, write, errors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)

if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()