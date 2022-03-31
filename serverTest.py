import socket
HOST = "0.0.0.0"
#HOST = "192.168.1.6"
PORT = 5555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected to", addr)
            data = conn.recv(1024)
            print("Received:", data.decode())
            conn.sendall(data)

if __name__ == '__main__':
    pass