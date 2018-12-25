#!/usr/bin/env python

import Pyro4
import dbUI


Pyro4.config.SERIALIZER = 'pickle'

def main():
        ns = Pyro4.locateNS(host="193.136.128.108", port=9090)
        uri = ns.list('BookDB')
        
        db = list()
        for key, val in uri.items():
        	if "80856" in str(val) or "81038" in str(val):
        		db.append(Pyro4.Proxy(val))
        
       	print (db)
       	ui = dbUI.dbUI(db[1])
       	ui.menu()

if __name__=="__main__":
        main() 
