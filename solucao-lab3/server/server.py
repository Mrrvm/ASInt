#!/usr/bin/env python

import Pyro4
import bookDB




Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

def main():
        remoteLibrary = Pyro4.expose(bookDB.bookDB)

        db = bookDB.bookDB("mylib")


        daemon = Pyro4.Daemon()

        ns = Pyro4.locateNS()
        print (ns)

        try:
                ns.createGroup(':libraries')
        except:
                pass

        uri = daemon.register(db, "BookDB")
        ns.register("BookDB", uri)

        try:
                daemon.requestLoop()
        finally:
                daemon.shutdown(True)

if __name__=="__main__":
        main() 
