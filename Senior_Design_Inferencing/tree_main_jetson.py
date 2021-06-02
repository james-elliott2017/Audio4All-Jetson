# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:49:51 2021

@author: james
"""

#UART Packages
import time
import serial
#I2C Packages
import os
import ast #used for str(list) -->
from I2C_example import i2c_out
from I2C_example import uart_to_list
from I2C_example import char_to_str

#Main File for Jetson Inference Package
from tree_imports import dataset
from tree_imports import word_to_ix
from tree_imports import ix_to_chord
from tree_imports import listToMidi

import tree_class
from tree_class import forest

class modelMain():
	def __init__(self):
		self.idx = 0 #index to decide if progression is over
		self.initial_flag = True #first pass has different calling
		self.chord_out = None #initial chord for sending purposes
		self.data_list = None
	def __modelcheck(self):
		if self.initial_flag == True:
            #grab starting chord
			if self.data_list in tree_bases:

			    base_index = tree_bases.index(self.data_list)
			    start_chord = tree_bases[base_index]
			else:
			    print("input not found, defaulting to first option")
			    start_chord = tree_bases[0]

			#create random version
			chordForest.update_current_tree(start_chord)
			self.random_prog = chordForest.random_chord_progression()
			self.idx += 1 #send next chord
			self.chord_out = self.random_prog[self.idx] #grab first chord

			self.initial_flag = False
		else:
			#check if user clicked the recommended chord from last session
			if self.chord_out == self.data_list and self.idx < 3:
			    print("Progression Followed")
			    self.idx += 1
			    self.chord_out = self.random_prog[self.idx]
			#progression completed check
			elif self.idx == 3 and self.chord_out == self.data_list:
				print("Progression Completed, checking for new progression\n\n")
				if self.data_list in tree_bases:
					base_index = tree_bases.index(self.data_list)
					start_chord = tree_bases[base_index]
				else:
					print("input not found, defaulting to first option")
					start_chord = tree_bases[0]
				#new progression & if self.idx == 3
				chordForest.update_current_tree(start_chord) #create new progression
				self.random_prog = chordForest.random_chord_progression()
				self.idx = 1
				self.chord_out = self.random_prog[self.idx]
			else:
			    if self.data_list in tree_bases:
			        base_index = tree_bases.index(self.data_list)
			        start_chord = tree_bases[base_index]
			    else:
			        print("input not found, defaulting to first option")
			        start_chord = tree_bases[0]
			    #new progression & if self.idx == 3
			    chordForest.update_current_tree(start_chord) #create new progression
			    self.random_prog = chordForest.random_chord_progression()
			    self.idx = 1
			    self.chord_out = self.random_prog[self.idx]
	def run_model(self,data_in):
		self.data_list = list(data_in)
		self.__modelcheck()
		return self.chord_out

def Main():
	serial_port = serial.Serial(
	    port="/dev/ttyTHS1",
	    baudrate=115200,
	    bytesize=serial.EIGHTBITS,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	)
	# Wait a second to let the port initialize
	time.sleep(1)
	model = modelMain()
	try:
		print("Loop Started")
		while True:
			if serial_port.inWaiting() > 0:
				data = serial_port.read()
				print(data)
				#convert to list
				chord_out = model.run_model(data)
				#data check
				if chord_out != None:
				    #call I2C function
				    i2c_out(list(chord_out)) #send data out
				else:
				    print("chord out doesn't exist")

	except KeyboardInterrupt:
	    print("Exiting Program")

	except Exception as exception_error:
	    print("Error occurred. Exiting Program")
	    print("Error: " + str(exception_error))

	finally:
	    serial_port.close()
	    pass

if __name__ == '__main__':
    #initialize datasets
    data = tree_class.dataset_converter(dataset)
    tree_bases = tree_class.extract_tree_bases(dataset)
    
    chordForest = forest(tree_bases,data,\
                         word_to_ix,ix_to_chord)
    #call main function
    Main()





 #    while True:
 #        #jetson only code##################################
 #        #code selects a starting chord from the tree_bases
 #        input_line = input("Input Number between 0-43: ")
 #        input_line = int(input_line)
	# ###################################################
 #        start_chord = tree_bases[input_line]
 #        chordForest.update_current_tree(start_chord)
    
 #        random_prog = chordForest.random_chord_progression()
 #        print(random_prog)
 #        listToMidi(random_prog,printOut=False)
