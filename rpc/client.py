import grpc
import Chat_pb2,Chat_pb2_grpc


class Client():
    def __init__(self,nombre):
        self.channel = grpc.insecure_channel('localhost:8080')
        self.stub = Chat_pb2_grpc.ChatStub(self.channel)
        self.id = self.stub.Connection(Chat_pb2.Nombre(nombre = 'nombre')).id # se le pide al server que nos de un id 
        print(f'El id que me dio el server es {self.id}')
    def Ping(self):
        respuesta = self.stub.Ping(
        Chat_pb2.Pong(
            ping = 'Miedo Potter ? '
            )
        )
        print(respuesta)

## se envia mensaje 
    def SendMessage(self,contenido,destino):
        try:
            self.stub.SendMessage(Chat_pb2.Message(
                contenido = "miedo potter ? ",
                timestamp = "intento",
                id = 3,
                receptor = "Mi mama"
            ))
        except grpc.RpcError as err:
            print(err)

    def ReciveMessage(self):
        for mensaje in self.stub.ReciveMessage(Chat_pb2.Empty()):
            emisor = mensaje.emisor
            print(f'[{emisor.nombre}#{emisor.id}-{mensaje.timestamp}]{mensaje.contenido}')

client = Client('Vicente ')
client.Ping()