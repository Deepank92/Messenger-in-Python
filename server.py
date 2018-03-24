#server.py

import socket
import threading


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234
clients = {}    #Dictionary used to keep track of clients connected to the server
serverRunning = True
soc.bind((ip, port))
soc.listen()
print('Server Ready')
print('IP Address of the server::'+ip)

#Thread Used to handle the client. For every client
#a new thread will be spawned
def handleClient(client, uname):
    clientConnected = True;
    key = clients.keys()
    help = 'There are four commands in Messenger\n1::**chatlist=>gives you the list of the people currently online\n2::**quit=>To end your session\n3::**broadcast=>To broadcast your message to each and every person currently present online\n4::Add the name of the person at the end of your message preceded by ** to send it to particular person'
    while(clientConnected):
        response = 'Number of People Online\n'
        msg = client.recv(1024).decode('ascii')

        if '**chatlist' in msg:
            clientNo = 0
            for name in key:
                clientNo += 1
                response = response + str(clientNo) +'::' + name+'\n'
            client.send(response.encode('ascii'))
        elif '**help' in msg:
            client.send(help.encode('ascii'))
        elif '**broadcast' in msg:
            msg = msg.replace('**broadcast','')
            for k,v in clients.items():
                v.send(msg.encode('ascii'))
        elif '**quit' in msg:
            response = 'Stopping Session and exiting...'
            client.send(response.encode('ascii'))
            clients.pop(uname)
            print(uname + ' has been logged out')
            clientConnected = False
        else:
            found = False
            for name in key:
                if('**'+name) in msg:
                    msg = msg.replace('**'+name, '')
                    clients.get(name).send(msg.encode('ascii'))
                    found = True
                    break
            if not found:
                client.send('Trying to send message to invalid person.'.encode('ascii'))

#Server main thread
#Always running and waiting for the client request
while serverRunning:
    client, address = soc.accept()
    uname = client.recv(1024).decode('ascii')
    print('%s has logged in'%(str(uname)))
    client.send('Welcome to Messenger. Type **help to know all the commands'.encode('ascii'))
    if client not in clients:
        clients[uname] = client
        threading.Thread(target=handleClient, args=(client,uname,)).start()