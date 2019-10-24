import grpc
import Chat_pb2,Chat_pb2_grpc
import threading
import time 

SERVER = 'localhost'
PORT = '8080'

class Client():

    def __init__(self,nombre):
        self.nombre = nombre 
        self.channel = grpc.insecure_channel(f'{SERVER}:{PORT}')
        self.stub = Chat_pb2_grpc.ChatStub(self.channel)
        self.id = self.stub.Connection(Chat_pb2.Nombre(nombre = nombre)).id # se le pide al server que nos de un id 
        self.my_user = Chat_pb2.User(
            id = self.id,
            nombre = self.nombre 
        )
        #se crea thread para que escuche los mensajes entrantes 
        threading.Thread(target=self.ReciveMessage,daemon=True).start()

#### Funcion de prueba 
    def Ping(self):
        respuesta = self.stub.Ping(
        Chat_pb2.Pong(
            ping = self.nombre
            )
        )
        print(respuesta)

## se envia mensaje 
    def SendMessage(self,contenido,destino):
        try:
            response = self.stub.SendMessage(Chat_pb2.Message(
                emisor = self.my_user,
                contenido = contenido,
                timestamp = "hora",
                receptor = Chat_pb2.User(
                    id = int(destino.split('#')[1]) ,#que aca sea estilo destino.id
                    nombre = destino.split('#')[0] #destino.nombre o algo asi 
                )
            ))
            print(f'La respuesta fue: {response}')
        except grpc.RpcError as err:
            print(err)
        

    def ReciveMessage(self):
        try:
            for mensaje in self.stub.ReciveMessage(Chat_pb2.Id(id = self.id)):
                emisor = mensaje.emisor
                print(f'[{emisor.nombre}#{emisor.id}-{mensaje.timestamp}]{mensaje.contenido}')
        except grpc.RpcError as err:
            print(err)



################ Loop Principal #########################
print('Ingrese su nombre de usuario: ',end = '')
nombre = input()

client = Client(nombre)
while True:
    print('Ingrese destinatario: ',end = '') # de la forma nombre#id
    destinatario  = input()
    print('Ingrese mensaje a enviar: ',end = '')
    mensaje = input() 
    client.SendMessage(mensaje,destinatario)