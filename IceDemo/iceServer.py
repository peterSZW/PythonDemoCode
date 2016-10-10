#coding=gbk
import sys, traceback, time, Ice
Ice.loadSlice('Hello.ice') #加载slice文件并编译，其实是把slice2py该干的事情都干好了，
                           #下面就直接用import Demo引入模块
import Demo
class PrinterI(Demo.Printer):#继承Printer接口
    def printString(self,str,current=None):#实现了接口的printString函数
        print str
class Server(Ice.Application):
    def run(self,args):
        if len(args)>1:
            print self.appName() + ": too many arguments"
            return 1
        adapter = self.communicator().createObjectAdapter("Printer")
        adapter.add(PrinterI(), self.communicator().stringToIdentity("Printer"))
        adapter.activate()
        self.communicator().waitForShutdown()
        return 0
sys.stdout.flush()
app=Server()
app.main(sys.argv,"config.server")
