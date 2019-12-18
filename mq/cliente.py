import pika
import threading
import socket
import json

RABBIT = 'localhost'
HOST = '0.0.0.0'
PORT = 5062


class Cliente:
    """docstring for Cliente."""
    def __init__(self, nombre):
        # INIT
        self.nombre = nombre
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.s.sendall(bytes(self.nombre, 'utf-8'))

        # RECIBE EL ID
        data = self.s.recv(1024)
        self.id = int(data.decode("utf-8"))

        # Se declara la cola
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        self.channel.queue_declare(queue= f'recive#{self.id}')
        threading.Thread(target=self.recive_message, daemon=True).start()

        print(f'mi id es {self.id}')

    def callback(self, ch, method, properties, body):
        print(" [x] %r" % body)

    # comando e {0,1,2} : 0 = send_message ; 1 == historial ; 2==list_user
    def send_message(self, receptor, message,comando ): 
        # Darle formato JSON/Diccionario
        nombre,id = receptor.split("#")
        mensaje = {}
        if comando == 0:
            mensaje = {
                    'tipo' : 0,
                    'body' : message,
                    'id_receptor' : id,
                    'nombre_receptor' : nombre,
                    'id_emisor' : self.id,
                    'nombre_emisor' : self.nombre
            }

        elif comando == 1:
            mensaje = {
                    'tipo' : 1,
                    'comando' : 'historial'
            }

        elif comando == 2:
            mensaje = {
                    'tipo' : 2,
                    'comando' : 'list_user'
            }

        msn = json.dumps(mensaje)
        print(f'Este es el mensaje {msn}')
        self.s.sendall(msn.encode())
        #self.channel.basic_publish(exchange='', routing_key=f'send#{receptor}',body=message)

    def recive_message(self):
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        channel = connection.channel()
        channel.basic_consume(queue=f'recive#{self.id}', on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()



if __name__ == "__main__":
    nombre = input("Ingrese su nombre: ")
    cliente = Cliente(nombre)
    while True:
        print('Formato mensaje : !msn:{detinatario}#{id}:{mensaje}')
        print('Formato comando listado : !listado')
        print('formato comando mensajes enviados : !mensajes')
        print('>> Ingrese accion: ',end = '')
        inp  = input()
        ln = inp.split(':')
        if((ln[0] == '!listado') and (len(ln)==1)):
            cliente.send_message(f'{cliente.nombre}#{str(cliente.id)}', '!listado', 2)
        elif((ln[0] == '!mensajes') and (len(ln)==1)):
            cliente.send_message('#','',1)
        elif((ln[0] == '!msn') and (len(ln)==3)):
            destinatario = ln[1]
            mensaje = ln[2]
            cliente.send_message(destinatario, mensaje,0 )
        else:
            print('>> formato incorrecto, intente de nuevo')
