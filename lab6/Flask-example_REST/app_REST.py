from flask import Flask
from flask import render_template
from flask import request

import requests


if __name__ == '__main__':

    while(1):
        command = input("add get1 get2 quit")
        if command.upper() == "ADD":
            number = input("Number = ")
            ToSend = {'number': number}
            r = requests.post('http://localhost:5000/API/addValue', json=ToSend)
        elif command.upper() == "QUIT":
            exit(0)
        elif command.upper() == "GET1":
            #number = input("Number = ")
            #p = {"value": number}
            r = requests.get("localhost:5000/API/value/7")
            print(r.text())


