import serial
import sys,time
import signal
from time import ctime,sleep
import glob,struct
from multiprocessing import Process,Manager,Array
import threading


class mSerial():
	ser = None
	def __init__(self):
		print self

	def start(self):
		self.ser = serial.Serial('/dev/ttyAMA0',115200,timeout=0)
	
	def device(self):
		return self.ser

	def serialPorts(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')
		result = []
		for port in ports:
			s = serial.Serial()
			s.port = port
			s.close()
			result.append(port)
		return result

	def writePackage(self,package):
		self.ser.write(package)
		sleep(0.01)

	def read(self,n):
		return self.ser.read(n)

	def readline(self):
		return self.ser.readline()

	def isOpen(self):
		return self.ser.isOpen()

	def inWaiting(self):
		return self.ser.inWaiting()

	def close(self):
		self.ser.close()
		
	
class zeropi():
	def __init__(self):
		print "init zeropi"
		signal.signal(signal.SIGINT, self.exit)
		self.manager = Manager()
		self.__selectors = self.manager.dict()
		self.buffer = []
		self.bufferIndex = 0
		self.message = "";
		self.isParseStart = False
		self.exiting = False
		self.isParseStartIndex = 0
		
	def start(self):
		self.device = mSerial()
		self.device.start()
		sleep(0.1)
		self.run()
	
	
	def excepthook(self, exctype, value, traceback):
		self.close()
		
	def run(self):
		sys.excepthook = self.excepthook
		th = threading.Thread(target=self.__onRead,args=(self.onParse,))
		th.start()
		
	def close(self):
		self.device.close()
		
	def exit(self, signal, frame):
		self.exiting = True
		sys.exit(0)
		
	def __onRead(self,callback):
		while True:
			if(self.exiting==True):
				break
			try:	
				if self.device.isOpen()==True:
					n = self.device.readline()
					if len(n)>0:
						callback(n)
					else:
						sleep(0.01)
				else:	
					sleep(0.5)
			except Exception,ex:
				print 'onRead...'+str(ex)
				#self.exiting = True;
				#self.close()
				sleep(0.01)
				
	def __writePackage(self,pack):
		self.device.writePackage('\n'+pack+'\n')

	def motorRun(self,port,speed):
		self.__writePackage('M21 D'+str(port)+' P'+str(speed))

	def stepperRun(self,port,speed):
		self.__writePackage('M51 D'+str(port)+' F'+str(speed))

	def stepperStop(self,port):
		self.__writePackage('M54 D'+str(port))

	def stepperMove(self,port,distance,speed,callback):
		self.__doCallback('R52 D'+str(port),callback)
		self.__writePackage('M52 D'+str(port)+' R'+str(distance)+' F'+str(speed))

	def stepperMoveTo(self,port,position,speed,callback):
		self.__doCallback('R52 D'+str(port),callback)
		self.__writePackage('M52 D'+str(port)+' A'+str(position)+' F'+str(speed))

	def stepperSetting(self,port,microstep,accelate):
		self.__writePackage('M53 D'+str(port)+' S'+str(microstep)+' A'+str(accelate))

	def servoRun(self,port,angle):
		self.__writePackage('M41 D'+str(port)+' A'+str(angle))
		
	def digitalWrite(self,pin,level):
		self.__writePackage('M11 D'+str(pin)+' L'+str(level))

	def pwmWrite(self,pin,pwm):
		self.__writePackage('M11 D'+str(pin)+' P'+str(level))

	def digitalRead(self,pin,callback):
		self.__doCallback('R12 D'+str(pin),callback)
		self.__writePackage('M12 D'+str(pin))
	
	def analogRead(self,pin,callback):
		self.__doCallback('R13 A'+str(pin),callback)
		self.__writePackage('M13 A'+str(pin))
	
	def onParse(self,msg):
		if len(msg)>3:
			if len(msg.split("OK"))>1:
				msg = "".join(("".join(msg.split("\r"))).split("\n"))
				if len(msg.split("L"))>1:
					if self.__selectors["callback_"+msg[0:(msg.index("L")-1)]]:
						self.__selectors["callback_"+msg[0:(msg.index("L")-1)]](int(msg.split("L")[1].split(" ")[0]));
				else:
					if self.__selectors["callback_"+msg[0:(msg.index("OK")-1)]]:
						self.__selectors["callback_"+msg[0:(msg.index("OK")-1)]]();
				
	def __doCallback(self, extID, callback):
		self.__selectors["callback_"+str(extID)] = callback
