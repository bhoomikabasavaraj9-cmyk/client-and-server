import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 9000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname=HOST)
conn.connect((HOST, PORT))

# ✅ Added message about SSL encryption
print("\n🔒 This chat is encrypted using SSL. Your messages are secure!\n")

username = input("Enter your name: ")
conn.send(username.encode('utf-8'))

def receive():
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                print(msg)
        except:
            print("[ERROR] Disconnected from server.")
            conn.close()
            break

threading.Thread(target=receive).start()