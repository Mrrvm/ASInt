from socket import *
import pickle
import lab2_module

s = socket(AF_INET, SOCK_STREAM)

host = gethostname()

port = 4120

s.connect((host, port))

s.send('push'.encode())
s.send(str(input('1st number: ')).encode())

s.send('push'.encode())
s.send(str(input('2nd number: ')).encode())

s.send('push'.encode())
s.send(str(input('3rd number: ')).encode())

s.send('addsub'.encode())

s.send('close'.encode())
Obj = pickle.loads(s.recv(1024))
Obj.print()

s.close();