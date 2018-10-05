from socket import *
import lab2_module

s = socket(AF_INET, SOCK_STREAM)

host = gethostname()

port = 4120

s.bind((host, port))

s.listen(5)

c, addr = s.accept()
Obj = lab2_module.rpnCalculator()
print('Connection from')
print(addr)

while True:
    ret = c.recv(32).decode()
    print(ret)
    if ret == 'push':
        ret = c.recv(32).decode()
        Obj.pushValue(int(ret))

    elif ret == 'addsub':
        Obj.AddSub()

    elif ret == 'close':
        break

Obj.print()
c.close()
