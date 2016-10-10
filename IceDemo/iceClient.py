import os,sys,traceback,Ice
Ice.loadSlice("Hello.ice")
import Demo
ic=Ice.initialize(sys.argv)
base=ic.stringToProxy("Printer:tcp -h 127.0.0.1 -p 50110")
printer=Demo.PrinterPrx.checkedCast(base)
if not printer:
       raise RuntimeError("Invalid proxy")
printer.printString("Hello World!")
ic.destroy()
