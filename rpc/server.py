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
        self.recibidos = {}
        self.nombre = []

    def Connection(self,request,context):
        print(f'Responde el thread{threading.get_ident()}')

        self.nombre.append(request.nombre) # se obtiene el nombre de la persona que hizo la request, supongo que despue slo ssamos ?
        new_id = self.user_id
        self.enviados[new_id] = [] # se crea llave = id , valor = lista de mensajes enviados
        self.recibidos[new_id] = [] #se crea lista para mensaje recibidos

        self.user_id+=1 #se deberia usar locks aca (?)


        return Chat_pb2.Id(id = new_id)

    def SendMessage(self,message,context):
        flag = False
        respuesta = Chat_pb2.Estado(
            estado = flag ,
            detalle = f'El mensaje a {message.receptor} no pudo se entregado'
        )
        if message.receptor.id > self.user_id and message.receptor.nombre not in self.nombre: #el usuario que iba a ser el enviado el mensaje no existe
            return respuesta


        self.recibidos[message.receptor.id].append(message)
        self.enviados[message.emisor.id].append(message)
        # Se procede a escribir log .txt
        f = open("log.txt","a")
        f.write(f'Sender [{message.emisor.nombre}#{message.emisor.id}] Receiver [{message.receptor.nombre}#{message.receptor.id}] Message [{message.id}:{message.contenido}:{message.timestamp}]\n')
        f.close()
        print(f'El usuario {message.emisor.nombre} envia mensaje a {message.receptor.nombre}')
        return Chat_pb2.Empty()

    def New_message(self,n,context):
        self.message_id+=1
        return Chat_pb2.NewMessageID(
            id = self.message_id
        )


    def Ping(self,pong,context):
        respuesta = pong.ping
        print(f'El cliente {respuesta} tiene estos nombres: {self.nombre}')
        return Chat_pb2.Pong(
            ping = 'Ni un Poco '
        )

    def ReciveMessage(self,id,context):
        ID = id.id
        while True:
            while len  (self.recibidos[ID]) != 0:
                yield self.recibidos[ID].pop(0)


if __name__ == "__main__":
    #Se corre server con n threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print("nueva hebra ")
    #se agrega la clase al servidor
    Chat_pb2_grpc.add_ChatServicer_to_server(Server(),server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print('API start ')
    while True:
        time.sleep(60)
