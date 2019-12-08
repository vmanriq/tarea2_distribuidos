import pika
import socket

from concurrent import futures

PORT = 5000
HOST = "0.0.0.0"

class ClientHanlder():
    def __init__(self,conn,addr):
        self.user_id = 0
        print("Se conecto:",addr)
        with conn:
            self.principal()
            data = conn.recv(1024)
            conn.sendall(b"Se recibio correctamente la peticion")
            registro.write(str(addr[0])+":"+repr(data)+"\n")
            registro.close()
    def principal(self):
        print("funciono")
        return

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    while True:
        conn, addr = s.accept()

        server  = futures.ThreadPoolExecutor(max_workers=10)
        f = server.submit(ClientHanlder,args=(conn,addr,))
