#I2C Code Example
#Not needed for inferencing
#import sys
#import os


if __name__ == '__main__':
	print("Test Run")
	import os
	import ast
	
	#test data, but will be passed later
	test_string = [12,24,16]

	stop_bit = "z"
	stop_byte = format(ord(stop_bit),'08b')

	data_in_num = []
	for note in data_in:
		data_in_num.append(int(bin(note)[2:],2))


	bus = 0
	teensy_address = 9
	for num in data_in_num:
		input_str = "i2cset -f -y {} {} {}".format(bus,teensy_address,num)
		print(input_str)
		os.system(input_str)

	print("Packet Sent")