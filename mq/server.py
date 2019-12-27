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

PORT = 5020
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
        print(f"Este es mi id {self.id}")


        self.conn = conn
        data = self.conn.recv(1024)


        self.nombre = data.decode('utf-8')

        print(f'Este es minombre {self.nombre}')

        USERS.addUser(f'{self.nombre}#{str(self.id)}')
        self.USERS = USERS

        # ENVIA EL ID ?¡
        self.conn.sendall(str(self.id).encode())
        self.conn.close()
        # CREA LAS COLAS
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        self.channel.queue_declare(queue= f'recive#{self.id}')

        threading.Thread(target=self.recive_message, daemon=True).start()
        #self.recive_message()

    def verificar(self, message):
        user = f"{message['nombre_receptor']}#{message['id_receptor']}"
        if user in USERS.getUsers():
            return True
        else:
            return False

    # comando e {0,1,2} : 0 = send_message ; 1 == historial ; 2 ==list_user
    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
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
                    'body' : 'Error, el usuario ingresado no existe',
                    'id_receptor' : message['id_emisor'],
                    'nombre_receptor' : message['nombre_emisor']
                }
        elif tipo == 1:
            message_list = []
            try:
                a = open("log/log.txt","r")
                for i in a:
                    m = json.loads(i.replace("\'","\"").strip())
                    if m['nombre_emisor'] == message['nombre_emisor'] :
                        message_list.append(m)
                a.close()
            except:
                print("Sin mensajes registrados")
            message = {
                'tipo' : 1,
                'body' : message_list,
                'id_receptor' : message['id_emisor'],
                'nombre_receptor' : message['nombre_emisor']
            }

        elif tipo == 2:
            message = {
                'tipo' : 2,
                'body' : self.USERS.getUsers(),
                'id_receptor' : message['id_emisor'],
                'nombre_receptor' : message['nombre_emisor']
            }
        self.send_message(message)

    def recive_message(self):
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        channel = connection.channel()
        #channel.basic_consume( queue=f'main' , on_message_callback=self.callback, auto_ack=True)
        channel.basic_consume( queue=f'send#{self.id}' , on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()



    def send_message(self, message):
        msn = json.dumps(message).encode()
        try:
            self.channel.basic_publish(exchange='', routing_key=f"recive#{message['id_receptor']}",
                                    body=msn)
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
        server.submit(ClientHanlder(conn, addr, IDS, USERS, IDM))
        IDS.update()
