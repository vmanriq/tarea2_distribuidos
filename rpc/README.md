# Para compilar proto

``` python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Chat.proto ```

# Para iniciar otro cliente, al hacer esto se ingresa automaticamente al container 
  docker-compose run client bash

# Para entrar a un cliente
  docker exec -it client{1,2} bash

# Para ejecutar el programa dentro del container

  python3 client.py

### To do

+ Arreglar si no hay mensajes enviados, avisar
+
