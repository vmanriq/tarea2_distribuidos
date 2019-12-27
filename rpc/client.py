import grpc
import Chat_pb2,Chat_pb2_grpc
import threading
import time



SERVER = 'server'
PORT = '8080'

class Client():

    def __init__(self,nombre):
        self.nombre = nombre
        self.channel = grpc.insecure_channel(f'{SERVER}:{PORT}')
        self.stub = Chat_pb2_grpc.ChatStub(self.channel)
        self.id = self.stub.Connection(Chat_pb2.Nombre(nombre = nombre)).id # se le pide al server que nos de un id
        print(f'Id cliente: {self.id}, Nombre Cliente: {self.nombre}')
        print('==================================BEGIN=======================================')
        self.my_user = Chat_pb2.User(
            id = self.id,
            nombre = self.nombre
        )
        #se crea thread para que escuche los mensajes entrantes
        threading.Thread(target=self.ReciveMessage,daemon=True).start()


## se envia mensaje
    def SendMessage(self,contenido,destino):
        try:
            response = self.stub.SendMessage(Chat_pb2.Message(
                emisor = self.my_user,
                contenido = contenido,
                timestamp = time.strftime("%c"),
                receptor = Chat_pb2.User(
                    id = int(destino.split('#')[1]) ,# que aca sea estilo destino.id
                    nombre = destino.split('#')[0] # destino.nombre o algo asi
                ),
                # Esto debería tener lock????
                id = self.stub.New_message(Chat_pb2.Id(id = self.id)).id
            ))
            if not response.flag:
                print("NO existe el usuario a quien se le quiere enviar el mensaje ")
        except grpc.RpcError as err:
            print(err)


    def ReciveMessage(self):
        try:
            for mensaje in self.stub.ReciveMessage(Chat_pb2.Id(id = self.id)):
                emisor = mensaje.emisor
                print('\n========================= NUEVO MENSAJE RECIBIDO ===============================')
                print(f'[{emisor.nombre}#{emisor.id}-{mensaje.timestamp}]{mensaje.contenido}')
                print('>> Ingrese accion:')
        except grpc.RpcError as err:
            print(err)

    def Messages(self):
        m = self.stub.Messages(Chat_pb2.Id(id = self.id))
        for i in m.msn:
            print(f'-> {i.contenido}')
        if len(m.msn) == 0:
            print('-> NO  mensajes enviados')

    def ListaDeUsuarios(self):
        m = self.stub.ListaDeUsuarios(Chat_pb2.Id(id = self.id))
        for i in m.user:
            print(f'-> Nombre Cliente {i.nombre}, Id cliente {i.id}')




################ Loop Principal #########################
print('>> Ingrese su nombre de usuario: ',end = '')
nombre = input()
client = Client(nombre)
while True:
    print('Formato mensaje : !msn:{detinatario}#{id}:{mensaje}')
    print('Formato comando listado : !listado')
    print('formato comando mensajes enviados : !mensajes')
    print('>> Ingrese accion: ',end = '')
    inp  = input()
    ln = inp.split(':')
    if((ln[0] == '!listado') and (len(ln)==1)):
        client.ListaDeUsuarios()
    elif((ln[0] == '!mensajes') and (len(ln)==1)):
        client.Messages()
    elif((ln[0] == '!msn') and (len(ln)==3)):
        destinatario = ln[1]
        mensaje = ln[2]
       # print(destinatario,mensaje)
        client.SendMessage(mensaje,destinatario)
    else:
        print('>> formato incorrecto, intente de nuevo')
