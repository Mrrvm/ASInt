from socket import *
import lab2_module
import pickle

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
    ret = c.recv(8).decode()
    print(ret)
    if ret == 'push':
        ret = c.recv(8).decode()
        Obj.pushValue(int(ret))

    elif ret == 'addsub':
        Obj.AddSub()

    elif ret == 'close':
        obj_serialized = pickle.dumps(Obj)
        c.send(obj_serialized)
        break

Obj.print()
c.close()
