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
        self.nombre = {}

    def Connection(self,request,context):
        print(f'Responde el thread{threading.get_ident()}')

        new_id = self.user_id
        self.nombre[new_id] = request.nombre # se obtiene el nombre de la persona que hizo la request, supongo que despue slo ssamos ?
        self.enviados[new_id] = [] # se crea llave = id , valor = lista de mensajes enviados
        self.recibidos[new_id] = [] #se crea lista para mensaje recibidos

        self.user_id+=1


        return Chat_pb2.Id(id = new_id)

    def SendMessage(self,message,context):
        flag = False
        respuesta = Chat_pb2.Estado(
            estado = flag ,
            detalle = f'El mensaje a {message.receptor} no pudo se entregado'
        )
        if message.receptor.id > self.user_id and message.receptor.nombre not in self.nombre.values(): #el usuario que iba a ser el enviado el mensaje no existe
            return Chat_pb2.Flag(flag=False)


        self.recibidos[message.receptor.id].append(message)
        self.enviados[message.emisor.id].append(message)
        # Se procede a escribir log .txt
        f = open("log/log.txt","a")
        f.write(f'Sender@[{message.emisor.nombre}#{message.emisor.id}]@Receiver@[{message.receptor.nombre}#{message.receptor.id}]@Message@[{message.id};{message.contenido};{message.timestamp}]\n')
        f.close()
        print(f'El usuario {message.emisor.nombre} envia mensaje a {message.receptor.nombre}')
        return Chat_pb2.Flag(flag=True)

    def New_message(self,n,context):
        self.message_id+=1
        return Chat_pb2.NewMessageID(
            id = self.message_id
        )




    def ReciveMessage(self,id,context):
        ID = id.id
        while True:
            while len  (self.recibidos[ID]) != 0:
                yield self.recibidos[ID].pop(0)

    def Messages(self,id,context):
        r = Chat_pb2.MessageList()
        try:
            f = open("log/log.txt","r")
            for i in f:
                l = i.split("@")
                if( int(l[1][1:-1].split("#")[1]) == id.id ):
                    men = l[5][1:-1].split(";")
                    r.msn.append(Chat_pb2.Message(
                                    id = int(men[0]),
                                    contenido = men[1],
                                    timestamp = men[2]
                    ))
            f.close()
        except:
            r.msn.append(Chat_pb2.Empty())
        return r

    def ListaDeUsuarios(self,id,context):
        r = Chat_pb2.UserList()
        for i in self.nombre:
            r.user.append(Chat_pb2.User(id = i, nombre = self.nombre[i]))
        return r


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
