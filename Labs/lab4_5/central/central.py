#!/usr/bin/env python

import dbUI
import bookDB

def main():

        db = bookDB.bookDB("mylib")
        ui = dbUI.dbUI(db)
        ui.menu()

if __name__=="__main__":
        main() 
