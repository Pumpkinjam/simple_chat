from socket import *
import os
import pickle


def print_log(chat_log : dict) -> None:
    for timestamp, content in chat_log.items():
        ip, message = content
        print(f'{ip} [{timestamp}] : {message}')


serverName = input('input server IP : ')
serverPort = int(input('input server Port : '))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send('\n\n'.encode())

if clientSocket.recv(1024).decode() == 'OK':
    print('connected.')
else:
    print('connection error.')
    raise Exception

clientSocket.close()

try:
    while True:
        msg = input('\n\n>>> ')

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        clientSocket.send(msg.encode())
        new_chat_log = pickle.loads(clientSocket.recv(2147483647))

        clientSocket.close()

        os.system('cls')# if '\\' in os.path else 'clear')
        print_log(new_chat_log)

except KeyboardInterrupt:
    clientSocket.send('\t\n'.encode())
    clientSocket.close()
    print('disconnected.')
    '''
except:
    clientSocket.send('\t\n'.encode())
    clientSocket.close()
    print('an error occurred.')
'''
