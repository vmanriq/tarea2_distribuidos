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
        self.usuarios = {}

    def AddMessage(self, body, usuario):
        self.usuarios[usuario].append(body)
    
    def GetMessages(self,usuario):
        return self.usuarios[usuario]

    def add(self, usuario):
        self.usuarios[usuario] = []

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
        print(f"Este es mi id {self.id}")
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

    # comando e {0,1,2} : 0 = send_message ; 1 == historial ; 2 ==list_user
    def recive_message(self):
        while True:
            data = self.conn.recv(1024)
            #data_decode = data.decode('utf-8')
            message = json.loads(data.decode('utf-8'))
            tipo = message['tipo']
            if tipo == 0:
                ne = message['nombre_emisor']
                ide = message['id_emisor']
                USERS.AddMessage( message['body'], f"{ne}#{str(ide)}"  )
                a = open("log.txt","a")
                a.write(str(message)+"\n")
                a.close()
                self.send_message(message)
            elif tipo == 1:
                l = []
                message = {
                    'tipo' : 1,
                    'id_receptor' : self.id,
                    'nombre_emisor' : self.nombre,
                    'body' : []
                }
                a = open("log.txt","r")
                for i in a:
                    m = json.loads(i.replace("\'","\"").strip())
                    print(m)
                    if m['nombre_emisor'] == self.nombre :
                        l.append(m['body'])
                a.close()
                message['body'] = l
                print(message)
                
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
                                    body=str(message['body']))
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
