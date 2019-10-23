from concurrent import futures
import grpc
import time 
import Chat_pb2
import Chat_pb2_grpc
import threading

class Server(Chat_pb2_grpc.ChatServicer):

    def __init__(self):
        self.user_id = 0
        self.message_id = 0
        self.enviados = {}
        self.nombre = []
    def Connection(self,request,context):
        print(f'Responde el thread{threading.get_ident()}')
        self.nombre.append(request.nombre) # se obtiene el nombre de la persona que hizo la request, supongo que despue slo ssamos ? 
        new_id = self.user_id
        self.enviados[new_id] = [] # se crea llave = id , valor = lista de mensajes enviados  
        self.user_id+=1
        return Chat_pb2.Id(id = new_id)
    
    def SendMessage(self,message,context):
        contenido = message.contenido
        print(f'El contendio del mensaje es: {contenido }')
        print(f'Este es mi nombre: {self.nombre}')
        return Chat_pb2.Empty()

    def Ping(self,pong,context):
        respuesta = pong.ping
        print(f'El cliente {respuesta} tiene estos nombres: {self.nombre}')
        return Chat_pb2.Pong(
            ping = 'Ni un Poco '
        )

    def ReciveMessage(self,request_iterator,context):
        
        while True:
            time.sleep(10)
            yield Chat_pb2.Message(
                contenido = "wena"
            )

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

