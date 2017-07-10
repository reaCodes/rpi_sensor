#!/usr/bin/python

import LCD1602
import time
import datetime
import dht11
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor


def buzz(buzzTime):

    GPIO_PIN = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)

    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(buzzTime)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    GPIO.cleanup()


def setup():

	#init(slave address, background light)
	LCD1602.init(0x27, 1)

	#DS18B20
	sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0416c0f87bff")
	#DHT11
	instance = dht11.DHT11(pin=16)

	#initial upper and lower limit
	min, max = 20, 30
    btnLD, btnLU, btnM, btnRD, btnRU = 21, 20, 26, 19, 13

	while True:

        #Setup GPIO for five keys
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btnLD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(btnLU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(btnM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(btnRD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(btnRU, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		#DS18B20
        temperature_in_celsius = sensor.get_temperature()
        #DHT11
        result = instance.read()
        
		#Set upper and lowwe limit
	    while GPIO.input(btnM) == 0:
            if GPIO.input(btnLD) == 0:
                min = min - 1
                #LCD1602.init(0x27, 1)
                LCD1602.write(0, 0, 'UPPER LIMIT: '+str(max)+' ')
                LCD1602.write(0, 1, 'LOWER LIMIT: '+str(min)+' ')
                time.sleep(0.1)
            elif GPIO.input(btnLU) == 0:
                min = min + 1
                #LCD1602.init(0x27, 1)
                LCD1602.write(0, 0, 'UPPER LIMIT: '+str(max)+' ')
                LCD1602.write(0, 1, 'LOWER LIMIT: '+str(min)+' ')
                time.sleep(0.1)
                
            elif GPIO.input(btnRD) == 0:
                max = max-1
                #LCD1602.init(0x27, 1)
                LCD1602.write(0, 0, 'UPPER LIMIT: '+str(max)+' ')
                LCD1602.write(0, 1, 'LOWER LIMIT: '+str(min)+' ')
                time.sleep(0.1)
            elif GPIO.input(btnRU) == 0:
                max = max+1
                #LCD1602.init(0x27, 1)
                LCD1602.write(0, 0, 'UPPER LIMIT: '+str(max)+' ')
                LCD1602.write(0, 1, 'LOWER LIMIT: '+str(min)+' ')
                time.sleep(0.1)
        
	    if temperature_in_celsius < float(min) or temperature_in_celsius > float(max):
            buzz(0.3)
		
	    LCD1602.write(0, 0, 'TEMPER: '+str(temperature_in_celsius)+'C   ')
	    #yeelink
        temp = '{"value":%f}'%temperature_in_celsius
        temp_output = open('/home/pi/temp_data.txt','w')
        temp_output.write(temp)
        temp_output.close
	    
	    if result.humidity!=0:
            LCD1602.write(0, 1, 'HUMIDITY: '+str(result.humidity)+'%   ')
            #yellink
            humi = '{"value":%f}'%result.humidity
            humi_output = open('/home/pi/humi_data.txt','w')
            humi_output.write(humi)
            humi_output.close

            
def loop():

    space = '                '
    greetings = 'Thank you for watching our homework! ^_^'
    greetings = space + greetings

    while True:
        
		tmp = greetings
		for i in range(0, len(greetings)):
		    LCD1602.write(0, 0, tmp)
		    tmp = tmp[1:]
		    time.sleep(0.1)
		    LCD1602.clear()


def destroy():
    
    pass


if __name__ == "__main__":
	
    try:
		setup()
		while True:
		    pass
    except KeyboardInterrupt:
		destroy()
