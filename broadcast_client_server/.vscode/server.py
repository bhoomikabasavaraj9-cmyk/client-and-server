import socket
import ssl
import threading

server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 9000

clients = {}

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
secure_sock=context.wrap_socket(server_socket, server_side=True)

control_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_server.bind((HOST, PORT))
control_server.listen()

print(f"[CONTROL] Server listening on {HOST}:{PORT}")

def broadcast(message, sender=None):
    print(f"[BROADCASTING] {message.decode('utf-8')}")
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()

def handle_client(client):
    try:
        username = client.recv(1024).decode('utf-8')
        clients[client] = username

        join_msg = f"[{username} has joined the chat]"
        print(f"[JOIN] {join_msg}")
        broadcast(join_msg.encode('utf-8'))

        while True:
            msg = client.recv(1024)
            if not msg:
                break
    except:
        pass
    finally:
        if client in clients:
            leave_msg = f"[{clients[client]} has left the chat]"
            print(f"[DISCONNECTED] {clients[client]}")
            broadcast(leave_msg.encode('utf-8'))
            del clients[client]
            client.close()

def accept_clients():
    while True:
        client_sock, addr = control_server.accept()
        conn = context.wrap_socket(client_sock, server_side=True)
        print(f"[NEW DATA CONNECTION] {addr} connected.")
        threading.Thread(target=handle_client, args=(conn,)).start()

def admin_input():
    while True:
        msg = input("Admin> ")
        if msg:
            broadcast(f"[ADMIN]: {msg}".encode('utf-8'))

threading.Thread(target=accept_clients).start()
admin_input()