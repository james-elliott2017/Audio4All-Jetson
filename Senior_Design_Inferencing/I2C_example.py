#I2C Code Example
#Not needed for inferencing
#import sys
#import os


if __name__ == '__main__':
	print("Test Run")
	import os
	import ast
	
	#test data, but will be passed later
	test_string = str([12,24,16])

	bus = 0
	teensy_address = 8
	input_str = "i2cset -f -y {} {} {}".format(bus,teensy_address,test_string)

	print(input_str)
	os.system(input_str)
	print("data sent")