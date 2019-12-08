class ClientHanlder():
    def __init__(self,conn,addr):
        self.user_id = 0
        print("Se conecto:",addr)
        with conn:
            data = conn.recv(1024)
            conn.sendall(b"Se recibio correctamente la peticion")
            registro.write(str(addr[0])+":"+repr(data)+"\n")
            registro.close()
