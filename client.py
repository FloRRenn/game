from socket import *
import threading

def client(ip, tunel, playerName):
    def reception():
        while True:
            try:
                message_recv = monSocket.recv(1024)
            except ConnectionResetError:
                break
            
            if not message_recv:  #Nếu kết nối được đóng bởi máy chủ
                break
            
            tunel.send(message_recv)
            
        print("Kết nối từ client đã bị ngắt")
        monSocket.close()

    def emission():
        while True:
            message_emis = tunel.recv()
            monSocket.send(message_emis)

    if ip == "0.0.0.0":  #
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 50000))
        while 1:
            data, ip_port = s.recvfrom(1500, 0)  #(b'Client OK', ('192.168.1.32', 62587))
            if data.decode() == "SuperS":
                break
            
        ip = ip_port[0]
        s.close()

    port = 5000

    #Thiết lập kết nối
    monSocket = socket()
    monSocket.connect((ip, port))
    monSocket.send(('P,' + playerName).encode())  #Gửi ký tự để xác nhận
    tunel.send(('P,' + playerName).encode())

    threadEmission = threading.Thread(target = emission)
    threadEmission.daemon = True
    threadReception = threading.Thread(target = reception)
    
    threadEmission.start()
    threadReception.start()
