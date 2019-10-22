import grpc
import Chat_pb2,Chat_pb2_grpc


class Client():
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:8080')
        self.stub = Chat_pb2_grpc.ChatStub(self.channel)


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

client = Client()
client.Ping()