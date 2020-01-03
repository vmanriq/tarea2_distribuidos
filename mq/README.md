# Tarea 2, sistemas distribuidos 2019-2020

## Integrantes
* Vicente Manriquez, 201673577-7
* Manuel Matus, 201673533-k

## Actividad 2, rabbitMQ Server

### Build & up
Para la ejecución de la primera actividad es necesario situarse en el directorio **./mq**
* build
> sudo docker-compose build
* up
> sudo docker-compose up

# Iniciar Clientes
  * Para entrar a uno de los dos clientes (desde otra consola), cada uno en una terminal separada 
  > docker exec -it client1 bash


  > docker exec -it client2 bash
  
  
  * Para ejecutar el código, en cada consola se debe hacer 
  
  
  > python3 cliente.py

# Para iniciar otro cliente
  * Iniciar cliente (al hacer esto se ingresa automáticamente al container)
  > docker-compose run client bash
  * y una vez dentro de la consola del container
  > python3 cliente.py
