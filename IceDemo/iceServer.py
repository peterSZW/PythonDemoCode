#coding=gbk
import sys, traceback, time, Ice
Ice.loadSlice('Hello.ice') #����slice�ļ������룬��ʵ�ǰ�slice2py�øɵ����鶼�ɺ��ˣ�
                           #�����ֱ����import Demo����ģ��
import Demo
class PrinterI(Demo.Printer):#�̳�Printer�ӿ�
    def printString(self,str,current=None):#ʵ���˽ӿڵ�printString����
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
