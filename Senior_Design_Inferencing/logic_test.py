# James Elliott
# Senior Design @ U.C. Davis --> Spring, 2021 (Audio4All)
# Inference Logic Testing for Chord Recommender (Binary Tree)
import numpy as np

#replace self.data_list with iinput
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

if __name__ == "__main__":
	print("\n\n\n\n")
	input_data = np.array([[55, 59, 62], [54, 57, 60], [64, 67, 71], [66, 69, 72]])
	in_chord = input_data[0]

	data = tree_class.dataset_converter(dataset)
	tree_bases = tree_class.extract_tree_bases(dataset)
    
	chordForest = forest(tree_bases,data,\
		word_to_ix,ix_to_chord)

	print("Test Data: ",input_data,"\n")
	model = modelMain()

	chord_out = model.run_model(in_chord)
	print(model.random_prog)
	print("Input: {}\nOutput: {}".format(in_chord,chord_out))

	for i in range(30):
		print("Input: {}".format(chord_out))
		chord_out = model.run_model(chord_out)
		print("Progression: ",model.random_prog)
		print("Output: {}".format(chord_out))
