import pika
import threading

RABBIT = 'localhost'

class Cliente:
    """docstring for Cliente."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.id = '1'
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
        self.channel.basic_consume(queue=f'recive#{self.id}', on_message_callback=self.callback, auto_ack=False)
        #print("WENA CARBOS ESTE EL THREAD \n \n \n")
        self.channel.start_consuming()



if __name__ == "__main__":
    nombre = input("Ingrese su nombre: ")
    cliente = Cliente(nombre)
    while True:
        print("Ingrese mensaje a enviar: ")
        mensaje = input()
        print("ingrese receptor: ")
        receptor = input()
        cliente.send_message(receptor, mensaje)
