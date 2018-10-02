import lab2_module


Obj = lab2_module.rpnCalculator()

print("First number")
Obj.pushValue(int(input("> ")))
print("Second number")
Obj.pushValue(int(input("> ")))
print("Third number")
Obj.pushValue(int(input("> ")))
print("Forth number")
Obj.pushValue(int(input("> ")))


Obj.print()

Obj.AddSub()

Obj.print()
