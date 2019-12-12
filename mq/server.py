import pika
import socket
import threading
import json
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
        #threading.Thread(target=self.recive_message, daemon=True).start()
        self.recive_message()

    def recive_message(self):
        while True:
            data = self.conn.recv(1024)
            #data_decode = data.decode('utf-8')
            message = json.loads(data.decode('utf-8'))
            tipo = message['tipo']
            if tipo == 0:
                a = open("log.txt","a")
                a.write(message)
                a.close()
                self.send_message(message)




    def send_message(self, message):
        # Esta weaita sería el decode del JSON/Diccionario

        try:
            self.channel.basic_publish(exchange='', routing_key=f'recive#{message.id_receptor}',
                                    body=message.body)
        except:
            print(f'El usuario {message.nombre_emisor} no existe')
        return


if __name__ == "__main__":
    IDS = 1
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    server  = futures.ThreadPoolExecutor(max_workers=10)
    while True:
        conn, addr = s.accept()
        f = server.submit(ClientHanlder(conn,addr,IDS))
        IDS+=1
