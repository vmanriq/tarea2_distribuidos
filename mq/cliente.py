import pika
import threading
import socket


RABBIT = 'localhost'
HOST = '0.0.0.0'
PORT = 5050


class Cliente:
    """docstring for Cliente."""
    def __init__(self, nombre):
        # INIT
        self.nombre = nombre
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.s.sendall(b'Iniciando Conexion')

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

    def send_message(self, receptor, message):
        # Darle formato JSON/Diccionario
        msn = receptor+"#"+mensaje
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
        print("Ingrese mensaje a enviar: ")
        mensaje = input()
        print("ingrese receptor: ")
        receptor = input()
        cliente.send_message(receptor, mensaje)
