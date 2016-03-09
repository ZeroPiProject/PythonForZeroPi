from lib.zeropi import *

def onRead(level):
	print level;

if __name__ == '__main__':
	bot = zeropi()
	bot.start()
	while 1:
		sleep(0.1);
		bot.analogRead(1,onRead);