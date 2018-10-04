from socket import *


s = socket(AF_INET, SOCK_STREAM)

host = gethostname()

port = 4120

s.bind((host, port))

s.listen(5)

c, addr = s.accept()

print 'Connection from', addr

while True:
	
	ret.clear()
	ret = c.recv(32)
	if ret == 'push':
		ret.clear()
		ret = c.recv(32)
		print (ret)

	elif ret == 'addsub':
		ret.clear()
		ret = c.recv(32)
		print ('hello')


c.close()