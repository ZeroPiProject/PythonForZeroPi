# Python For ZeroPi
* prepare your ZeroPi board. ( install the Firmware: https://github.com/ZeroPiProject/ZeroPi_Firmware)
* git clone https://github.com/ZeroPiProject/PythonForZeroPi on your Raspberry Pi
* Enter the folder "PythonForZeroPi", and **sudo python** digitalWrite.py

## Example
```
from lib.zeropi import *
if __name__ == '__main__':
	bot = zeropi()
	bot.start()
	while True:
		sleep(0.2);
		bot.digitalWrite(13,1);
		sleep(0.2);
		bot.digitalWrite(13,0);
```
## Python API
* **zeropi**()
* **start**()

### GPIO
* **digitalWrite** ( Pin, Level ) 
* **pwmWrite** ( Pin, Pwm )  
* **digitalRead** ( Pin, **def** onRead )
* **analogRead** ( Pin, **def** onRead )
 
### DC Motor
* **motorRun** ( Device, Pwm ) 
 * Device : 0 = Slot1( 1A+,1A- ), 1 = Slot1( 1B+,1B- ), ... , 6 = Slot4( 4A+,4A- ), 7 = Slot4( 4B+,4B- )  
 * Pwm : -255 ~ 255

### Servo Motor
* **servoRun** ( Pin, Angle)
 * Pin : 0 - 8 ( A0, A1, A2, A3, MO, MI, SCK, SDA, SCL )
 * Angle : 0 ~ 180

### Stepper Motor
* **stepperRun**( Device, Speed )
 * Device : 0 ~ 3 ( Slot1~4 )
 * Speed : 0 ~ 20000
* **stepperStop** ( Device )
* **stepperMove** ( Device, Distance, Speed, **def** onFinish )
* **stepperMoveTo** ( Device, Position, Speed, **def** onFinish )
* **stepperSetting** ( Device, Microstep, Accelation )
 * Microstep : 1, 2, 4, 8, 16
 * Accelation : 100 ~ 10000
