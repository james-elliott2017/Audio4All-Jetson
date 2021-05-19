#playground for Jetson Nano testing
import ast

data_in = "[51,42,63]"

list_in = ast.literal_eval(data_in)
test_equal = [51,42,63]
assert list_in == test_equal, 'not matching'
print("Type: {}, Data: {}".format(type(list_in),list_in))

print(list_in[1])