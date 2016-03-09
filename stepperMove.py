from lib.zeropi import *

def onForwardFinish():
	sleep(0.3);
	bot.stepperMove(1,-2000,2000,onBackwardFinish);

def onBackwardFinish():
	sleep(0.3);
	bot.stepperMove(1,2000,2000,onForwardFinish);

if __name__ == '__main__':
	bot = zeropi()
	bot.start()
	sleep(1);
	bot.stepperSetting(1,4,5000);
	bot.stepperStop(1);
	onForwardFinish();
	while 1:
		continue;