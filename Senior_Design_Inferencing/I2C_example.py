#I2C Code Example
#Not needed for inferencing
import sys
import os
import ast

def i2c_out(chord_list,stop_bit = "z",bus = 0, teensy_address=8):
	stop_byte = int(format(ord(stop_bit),'08b'),2)
	print("Stop Byte: {}".format(stop_byte))

	chord_list = ast.literal_eval(chord_list)
	##########################################################################
	for num in chord_list:
		input_str = "i2cset -f -y {} {} {}".format(bus,teensy_address,num)
		print(input_str)
		os.system(input_str)
	input_str = "i2cset -f -y {} {} {}".format(bus,teensy_address,stop_byte)
	os.system(input_str)
	##########################################################################
def char_to_str(str_list):
	final_string = ""
	for char in str_list:
		final_string += str(char)
	return final_string
def uart_to_list(string_list):
	data_str = string_list
	#remove whitespace
	data_str.replace(" ","")
	#convert to list of strings
	data_list =  data_str.strip('][').split(',')
	#make list of ints()
	int_list = [int(x) for x in data_list]
	return int_list

if __name__ == '__main__':
	print("START")
	import os
	import ast
	
	#test data, but will be passed later
	test_string = [12,24,16]

	i2c_out(test_string)

	print("Packet Sent")
