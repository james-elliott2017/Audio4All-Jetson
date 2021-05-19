#!/usr/bin/python3
import time
import serial
import codecs
import os
import sys
import ast
from I2C_example import i2c_out

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")

def char_to_str(str_list):
	final_string = ""
	for char in str_list:
		final_string += str(char)
	return final_string
#################################################
serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

try:
    # Send a simple header
    #serial_port.write("UART Demonstration Program\r\n".encode())
    #serial_port.write("NVIDIA Jetson Nano Developer Kit\r\n".encode())
    print("Waiting for Mail")
    char_list = ["none"]
    while True:
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            #print("Message Received")
            data = str(codecs.decode(data,"UTF-8")).replace(" ","")
            #print(data)
            if data == "[":
            	char_list[0] = data
            elif char_list[0] == "[" and data == "]":
            	char_list.append(data)
            	#print("Package Collected:\n{}".format(char_list))
            	lst = char_to_str(char_list)
            	print(type(lst))
            	print("List Version: {}".format(lst))
            	i2c_out(lst)
            	char_list = ["none"]
            elif char_list[0] == "[":
            	char_list.append(data)

            #serial_port.write(data)
            # if we get a carriage return, add a line feed too
            # \r is a carriage return; \n is a line feed
            # This is to help the tty program on the other end 
            # Windows is \r\n for carriage return, line feed
            # Macintosh and Linux use \n
            #if data == "\r".encode():
            #    # For Windows boxen on the other end
            #    serial_port.write("\n".encode())


except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
