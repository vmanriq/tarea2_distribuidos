from concurrent import futures
import grpc
import time 
import Chat_pb2
import Chat_pb2_grpc

class Server(Chat_pb2_grpc.ChatServicer):
    
    def SendMessage(self,message,context):
        contenido = message.contenido 
        emisor = message.emisor
        receptor = message.receptor 
        print(f'El nombre del emisor es {emisor}\n El nomde del receptor es: {receptor}')
        return 


if __name__ == "__main__":
    #Se corre server con n threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    #se agrega la clase al servidor
    Chat_pb2_grpc.add_ChatServicer_to_server(Server(),server)
    server.add_insecure_port('0.0.0.0:8080')
    server.start()
    print('API start ')
    while True:
        time.sleep(60)

