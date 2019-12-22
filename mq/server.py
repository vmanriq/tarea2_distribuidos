import pika
import socket
import threading
import json
from concurrent import futures

class id_message:
    def __init__(self):
        self.id = 0
    def getIdMessage(self):
        self.id += 1
        return self.id

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

    def addUser(self, usuario):
        self.usuarios.append(usuario)

    def getUsers(self):
        return self.usuarios

PORT = 5062
HOST = 'rabbitmqserver'
RABBIT = 'rabbitmq'
IDS = Id()
USERS = Users()
IDM = id_message() 

class ClientHanlder():
    def __init__(self, conn, addr, ID, USERS, IDM):
        # INIT
        self.id = ID.get()
        self.IDM = IDM
        self.conn = conn
        data = self.conn.recv(1024)
        self.nombre = data.decode('utf-8')
        USERS.addUser(f'{self.nombre}#{str(self.id)}')
        self.USERS = USERS
        # ENVIA EL ID ?¡
        self.conn.sendall(str(self.id).encode())

        # CREA LAS COLAS
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        self.channel.queue_declare(queue= f'recive#{self.id}')
        threading.Thread(target=self.recive_message, daemon=True).start()

    # comando e {0,1,2} : 0 = send_message ; 1 == historial ; 2 ==list_user
    def recive_message(self):
        while True:
            # JSON CON EN BINARY STRING DESDE CLIENTE
            data = self.conn.recv(1024)
            # DESERIALIZE
            message = json.loads(data.decode('utf-8'))
            tipo = message['tipo']
            if tipo == 0:
                if self.verificar(message) == True:
                    message['id_message'] = IDM.getIdMessage()
                    a = open("log/log.txt","a")
                    a.write(str(message)+"\n")
                    a.close()
                else:
                    message = {
                        'tipo' : 4,
                        'body' : 'Error, el usuario ingresado no existe'
                    }
            elif tipo == 1:
                message_list = []
                try:
                    a = open("log/log.txt","r")
                    for i in a:
                        m = json.loads(i.replace("\'","\"").strip())
                        if m['nombre_emisor'] == self.nombre :
                            message_list.append(m)
                    a.close()
                except:
                    print("No existen mensajes registrados")
                message = {
                    'tipo' : 1,
                    'body' : message_list
                }                
            elif tipo == 2:
                message = {
                    'tipo' : 2,
                    'body' : self.USERS.getUsers(),
                }    
            self.send_message(message)

    def send_message(self, message):
        msn = json.dumps(message).encode()
        try:
            if(message['tipo']==0):
                self.channel.basic_publish(exchange='', routing_key=f"recive#{message['id_receptor']}",
                                    body=msn)
            else:
                self.channel.basic_publish(exchange='', routing_key=f"recive#{str(self.id)}",
                                    body=msn)
        except:
            print(f"El usuario {message['nombre_emisor']} no existe")
        return
    
    def verificar(self, message):
        user = f"{message['nombre_receptor']}#{message['id_receptor']}"
        if user in USERS.getUsers():
            return True
        else:
            return False



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    while True:
        server  = futures.ThreadPoolExecutor(max_workers=10)
        conn, addr = s.accept()
        server.submit(ClientHanlder(conn, addr, IDS, USERS, IDM))
        IDS.update()
