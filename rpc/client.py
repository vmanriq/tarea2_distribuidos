import grpc
import Chat_pb2,Chat_pb2_grpc
import threading
import time 

class Client():
    def __init__(self,nombre):
        self.nombre = nombre 
        self.channel = grpc.insecure_channel('localhost:8080')
        self.stub = Chat_pb2_grpc.ChatStub(self.channel)
        self.id = self.stub.Connection(Chat_pb2.Nombre(nombre = nombre)).id # se le pide al server que nos de un id 
        self.my_user = Chat_pb2.User(
            id = self.id,
            nombre = self.nombre 
        )
        #se crea thread para que escuche los mensajes entrantes 
        threading.Thread(target=self.ReciveMessage,daemon=True).start()


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
            self.stub.SendMessage(Chat_pb2.Message(
                emisor = self.my_user,
                contenido = "miedo potter ? ",
                timestamp = "intento",
                receptor = Chat_pb2.User(
                    id = 3 ,#que aca sea estilo destino.id
                    nombre = 'receptor' #destino.nombre o algo asi 
                )
            ))
        except grpc.RpcError as err:
            print(err)

    def ReciveMessage(self):
        try:
            for mensaje in self.stub.ReciveMessage(Chat_pb2.Empty()):
                emisor = mensaje.emisor
                print(f'[{emisor.nombre}#{emisor.id}-{mensaje.timestamp}]{mensaje.contenido}')
        except grpc.RpcError as err:
            print(err)
print('Ingrese su nombre de usuario: ',end = '')
nombre = input()

client = Client(nombre)
client.SendMessage('contenido','vicente')
while True:
    client.Ping()
    time.sleep(10)