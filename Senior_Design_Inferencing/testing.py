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



# ''.join(bin(ord(c)) for c in string).replace('b','')