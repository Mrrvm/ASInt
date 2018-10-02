
class rpnCalculator:
    'Calculator for lab2'

    def __init__(self):
        self.stack = []


    def pushValue(self, x):
        self.stack.append(x)

    def popValue(self):
        return self.stack.pop()

    def AddSub(self):
        x = self.popValue()
        y = self.popValue()
        self.pushValue(x+y)

    def print(self):
        print(self.stack)
