import grpc

import Chat_pb2_grpc,Chat_pb2


SERVER_ADDRESS = '0.0.0.0'
PORT = '8080'

class Client():
    def __init__(self,nombre):
        self.nombre = nombre 
    
    def run(self):
        channel = grpc.insecure_channel(SERVER_ADDRESS+':'+PORT)
        
        ##se comunica por el stub ? 
        stub = Chat_pb2_grpc.ChatStub(channel) 

