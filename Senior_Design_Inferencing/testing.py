#playground for Jetson Nano testing
import ast

data_in = [51,42,63]

# list_in = ast.literal_eval(data_in)
# test_equal = [51,42,63]
# assert list_in == test_equal, 'not matching'
# print("Type: {}, Data: {}".format(type(list_in),list_in))

# print(list_in[1])

stop_bit = "z"
stop_byte = format(ord(stop_bit),'08b')

data_in_byte_array = []
data_in_num = []
for note in data_in:
	data_in_byte_array.append(bin(note)[2:])
	data_in_num.append(int(bin(note)[2:],2))

print("Chord: {}".format(data_in_byte_array))
print("Chose (10): {}".format(data_in_num))
print("Data Type: {}\n".format(type(data_in_byte_array[0])))
print("Stop Byte: ",stop_byte)
print("Base 10  : {}".format(int(stop_byte,2)))

#convert each num in list too base 10
	#data_in_num = []
	#for note in test_string:
	#	data_in_num.append(int(bin(note)[2:],2))


print("\n\nstring to list test:\n")
data_str = "[51, 42, 63]"
print("Original: ",data_str)
data_str.replace(" ","")
print("No Whitespace: ",data_str)

data_list =  data_str.strip('][').split(',')
print(data_list)
print("as ints")
int_list = [int(x) for x in data_list]
print(int_list)

print(ast.literal_eval(data_str))



