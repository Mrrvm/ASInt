#!/usr/bin/env python

import Pyro4
import bookDB




Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

def main():
        remoteLibrary = Pyro4.expose(bookDB.bookDB)

        db = bookDB.bookDB("mylib")


        daemon = Pyro4.Daemon(host="194.210.234.35")

        print (daemon)

        ns = Pyro4.locateNS(host="193.136.128.108", port=9090)
        print (ns)

        try:
                ns.createGroup(':libraries')
        except:
                pass

        uri = daemon.register(db, "BookDB-80856")
        ns.register("BookDB-80856", uri)

        try:
                daemon.requestLoop()
        finally:
                daemon.shutdown(True)

if __name__=="__main__":
        main() 
