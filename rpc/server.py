from concurrent import futures
import grpc
import time 
import Chat_pb2
import Chat_pb2_grpc

class Server(Chat_pb2_grpc.ChatServicer):

    def __init__(self):
        self.user_id = 0
        self.message_id = 0

    def Connection(self,request,context):
        nombre = request.nombre # se obtiene el nombre de la persona que hizo la request, supongo que despue slo ssamos ? 
        new_id = self.user_id

        self.user_id+=1
        return Chat_pb2.Id(id = new_id)
    
    def SendMessage(self,message,context):
        contenido = message.contenido
        print(f'El contendio del mensaje es: {contenido }')
        return Chat_pb2.Empty()

    def Ping(self,pong,context):
        respuesta = pong.ping
        print(f'El cliente envio {respuesta}')
        return Chat_pb2.Pong(
            ping = 'Ni un Poco '
        )

    def ReciveMessage(self,context):
        while True:
            pass

if __name__ == "__main__":
    #Se corre server con n threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #se agrega la clase al servidor
    Chat_pb2_grpc.add_ChatServicer_to_server(Server(),server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print('API start ')
    while True:
        time.sleep(60)

