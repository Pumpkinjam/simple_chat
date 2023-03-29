from socket import *
import time
import pickle

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# ip_dict records ip and the latest timestamp
ip_dict = dict()

# dictionary of chat_log follows the following format :
# { Timestamp : (ip, message) }
chat_log = dict()

print('Server Init OK')

while True:
    connectionSocket, addr = serverSocket.accept()
    payload = connectionSocket.recv(8192)
    payload = payload.decode()

    print(f'Connection from {addr[0]}')
    print(f'  payload : "{payload}"')

    if payload == '\n\n':       # payload only having two lf means the new participant
        connectionSocket.send('OK'.encode())
        ip_dict[addr[0]] = time.time()
        print(f'{addr[0]} joined the chat.')
        print(f'current : {ip_dict}')
    elif payload == '\t\n':     # payload with \t\b means the participant's quit
        print(f'{addr[0]} has left the chat.')
        del ip_dict[addr[0]]
        print(f'current : {ip_dict}')
    else:                       # this is just a normal chatting message
        ip_dict[addr] = timestamp = time.time()
        chat_log[timestamp] = (addr[0], payload)
        connectionSocket.send(pickle.dumps(chat_log))

    connectionSocket.close()
    