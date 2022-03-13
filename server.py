import time
from socket import *
import threading

def connectionAgain(): #Khôi phục lại kết nối khi bị mất
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
        s.sendto("GameOK".encode(), ('<broadcast>', 50000))
        time.sleep(1)

# Khỏi tạo server để nhận data từ client
def server():
    def gestionDuClient(conn, idConnThread):
        while 1:
            try:
                msgClient = conn.recv(1024)
                if msgClient == b'':
                    break
                
                #Gửi data cho tất cả client, trừ server
                for cle in conn_client:
                    if cle != idConnThread:
                        conn_client[cle].send(msgClient)
                        
                if msgClient.decode()[0] == 'F':
                    break
                
            except:
                pass
            
            
        #Đóng kết nối
        conn.close() #Ngắt kết nối đến server 
        del conn_client[idConnThread]  #Xóa client

    host = ""
    port = 5000

    serverSocket = socket()
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        serverSocket.bind((host, port))
    except Exception as e:
        print("Kết nối thất bại: ", e)
        
    else:
        print("Khởi tạo kết nối thành công! Đang chờ client kết nối đến....")
        serverSocket.listen(5)
        
        #Chờ đợi kết nối từ client
        conn_client = {}  #Tạo danh sách các client kết nối
        idConn = 1
        
        while 1:
            connection, address = serverSocket.accept()
            #Tạo luồng kết nối từ server đến client
            threadClient = threading.Thread(target = gestionDuClient, args = (connection, idConn))
            threadClient.start()
            
            #Lưu client vừa kết nối vào danh sách các client
            conn_client[idConn] = connection
            print("Server -> Client " + str(idConn) + " - IP : " + address[0] + ", port : " + str(address[1]))
            idConn += 1
            
if __name__ == "__main__":
    server()