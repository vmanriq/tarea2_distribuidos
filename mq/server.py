import pika
import socket
import threading

from concurrent import futures

PORT = 5050
HOST = "0.0.0.0"
RABBIT = 'localhost'

class ClientHanlder():
    def __init__(self,conn,addr,id):
        # INIT
        self.id = id
        self.conn = conn
        data = self.conn.recv(1024)

        # ENVIA EL ID ?¡
        self.conn.sendall(str(id).encode())

        # CREA LAS COLAS
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        self.channel.queue_declare(queue= f'recive#{self.id}')
        threading.Thread(target=self.recive_message, daemon=True).start()

    def recive_message(self):
        while True:
            data = self.conn.recv(1024)
            self.send_message(self, data)


    def send_message(self, C ,body):
        # Esta weaita sería el decode del JSON/Diccionario
        message = body.decode("utf-8").split("#")
        self.channel.basic_publish(exchange='', routing_key=f'recive#{message[0]}',
                                    body=message[1])
        return


if __name__ == "__main__":
    IDS = 1
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        server  = futures.ThreadPoolExecutor(max_workers=10)
        f = server.submit(ClientHanlder(conn,addr,IDS))
        IDS+=1
