from socket import *

s = socket(AF_INET, SOCK_STREAM)

host = gethostname()

port = 4120

s.connect((host, port))

s.send('push')
s.send(str(input('1st number: ')))

s.send('push')
s.send(str(input('2nd number: ')))

s.send('push')
s.send(str(input('3rd number: ')))

s.send('addsub')

s.close();