import RPi.GPIO as GPIO  #导入库
import time
import sys
import serial

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21

ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
def recv(ser):
        while True:
                data=bytes.decode(ser.read())
                #print('one'+data);
                if data=='':
                        continue
                else:
                        break
                sleep(0.02)
                serial.fiushInput()
        return data




def t_up(speed,t_time):                  #前进
        L_Motor.ChangeDutyCycle(speed)   #改变占空比
        GPIO.output(AIN2,False)#AIN2      #设置一个GPIO口的输出值
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)                		#暂停时间

def t_down(speed,t_time):						#同上
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):						#同上
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):						#同上
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def keysacn():
    val = GPIO.input(BtnPin)			#读取BtnPin的值给val
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)				#暂停0.01秒
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)			#设置Rpin的输出值为高电平
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)		#设置Rpin的输出值为低电平
        else:
            GPIO.output(Rpin,0)

def setup():
    GPIO.setwarnings(False)			#清除提示警告
    GPIO.setmode(GPIO.BCM)       # 树莓派电路板编号
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.setup(Gpin, GPIO.OUT)     # 让Gpin做为输出
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 上拉或下拉电阻


    GPIO.setup(AIN2,GPIO.OUT)
    GPIO.setup(AIN1,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)

    GPIO.setup(BIN1,GPIO.OUT)
    GPIO.setup(BIN2,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)

def checkdist():

        return 78
def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)


	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100


def control_car(ser):

    while True:
        data=recv(ser)
        time.sleep(0.1)
        #print("信号"+data)
        if data == 'exit':
            break
        elif data != 'exit' and data != '':
            if data == '2':
                print('前进')
                t_up(50,0)
                distance='%.2f' % checkdist()
                ser.write(distance.encode('GBK'))
            elif data == '5':
                print('后退')
                t_down(50,0.4)
                distance = '%.2f' % checkdist()
                ser.write(distance.encode('GBK'))
            elif data == '4':
                print('左转')
                t_left(50,0)
                distance = '%.2f' % checkdist()
                ser.write(distance.encode('GBK'))
            elif data == '6':
                print('右转')
                t_right(50,0)
                distance = '%.2f' % checkdist()
                ser.write(distance.encode('GBK'))
            elif data == '1':
                print('刹车')
                t_stop(0.3)
                distance = '%.2f' % checkdist()
                ser.write(distance.encode('GBK'))
        else:
            pass
def loop():
        while True:
                dis = distance()
                print dis, 'cm'
                print ''

try:
        setup()
        keysacn()
        loop() #冲突
        L_Motor= GPIO.PWM(PWMA,100)
        L_Motor.start(0)
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        control_car(ser)

except KeyboardInterrupt:
        ser.close();
        GPIO.cleanup() 			#清空(结束程序)
