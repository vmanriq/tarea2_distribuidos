import pika
import socket
import threading
import json
from concurrent import futures
class Id:
    def __init__(self):
        self.id = 0
    def update(self):
        self.id+=1
    def get(self):
        return self.id 
class Users:
    def __init__(self):
        self.usuarios = []
    def add(self, usuario):
        self.usuarios.append(usuario)
    def get(self):
        return self.usuarios

PORT = 5062
HOST = "0.0.0.0"
RABBIT = 'localhost'
IDS = Id()
USERS = Users()

class ClientHanlder():
    def __init__(self, conn, addr, ID, USERS):
        # INIT
        self.id = ID.get()
        print(f"Este es mi id{self.id}")
        self.conn = conn
        data = self.conn.recv(1024)
        self.nombre = data.decode('utf-8')
        print(f'Este es minombre {self.nombre}')
        USERS.add(f'{self.nombre}#{str(self.id)}')
        self.USERS = USERS
        # ENVIA EL ID ?¡
        self.conn.sendall(str(self.id).encode())

        # CREA LAS COLAS
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        self.channel.queue_declare(queue= f'recive#{self.id}')
        threading.Thread(target=self.recive_message, daemon=True).start()
        #self.recive_message()

    def recive_message(self):
        while True:
            data = self.conn.recv(1024)
            #data_decode = data.decode('utf-8')
            message = json.loads(data.decode('utf-8'))
            tipo = message['tipo']
            if tipo == 0:
                a = open("log.txt","a")
                a.write(str(message))
                a.close()
                self.send_message(message)
            elif tipo == 2:
                message = {
                    'tipo' : 2,
                    'body' : str(self.USERS.get()),
                    'id_receptor' : self.id,
                    'nombre_receptor' : self.nombre,
                    'id_emisor' : self.id,
                    'nombre_emisor' : self.nombre
            }    
                self.send_message(message)




    def send_message(self, message):
        # Esta weaita sería el decode del JSON/Diccionario

        try:
            self.channel.basic_publish(exchange='', routing_key=f"recive#{message['id_receptor']}",
                                    body=message['body'])
        except:
            print(f"El usuario {message['nombre_emisor']} no existe")
        return


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    #server  = futures.ThreadPoolExecutor(max_workers=10)
    while True:
        print(IDS.get())
        server  = futures.ThreadPoolExecutor(max_workers=10)
        conn, addr = s.accept()
        server.submit(ClientHanlder(conn, addr, IDS, USERS))
        IDS.update()
