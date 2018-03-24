import socket
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
clientRunning = True
uname = input('Enter user name::')
ip = input('Enter IP Address::')
soc.connect((ip, port))
msg = uname
soc.send(msg.encode('ascii'))

def handleListener(soc):
    while clientRunning:
        msg = soc.recv(1024).decode('ascii')
        print(msg)

threading.Thread(target=handleListener, args=(soc,)).start()

while(clientRunning):
    msg = input()
    if '**quit' in msg:
        clientRunning = False
        soc.send('**quit'.encode('ascii'))
    else:
        soc.send((uname+'>>' + msg).encode('ascii'))