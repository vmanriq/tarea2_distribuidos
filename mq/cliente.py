import pika
import threading

RABBIT = 'localhost'

class Cliente:
    """docstring for Cliente."""
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        #self.id = get_id()
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        self.channel = connection.channel()
        ###
        self.channel.queue_declare(queue= f'send#{self.id}')
        self.channel.queue_declare(queue= f'recive#{self.id}')
        threading.Thread(target=self.recive_message, daemon=True).start()
        #self.channel.queue_declare(exchange='send', queue= self.id)
        print(f'mi id es {self.id}')
    def callback(self, ch, method, properties, body):
        print(" [x] %r" % body)

    def send_message(self, receptor, message):
        self.channel.basic_publish(exchange='', routing_key=f'recive#{receptor}',
                                    body=message)

    def recive_message(self):
        connection =  pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
        channel = connection.channel()
        channel.basic_consume(queue=f'recive#{self.id}', on_message_callback=self.callback, auto_ack=True)
        #print("WENA CARBOS ESTE EL THREAD \n \n \n")
        channel.start_consuming()



if __name__ == "__main__":
    nombre = input("Ingrese su nombre: ")
    id = input("INgrese id: ")
    cliente = Cliente(nombre, id )
    while True:
        print("Ingrese mensaje a enviar: ")
        mensaje = input()
        print("ingrese receptor: ")
        receptor = input()
        cliente.send_message(receptor, mensaje)
