# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:49:51 2021

@author: james
"""

#UART Packages


#Main File for Jetson Inference Package
from tree_imports import dataset
from tree_imports import word_to_ix
from tree_imports import ix_to_chord
from tree_imports import listToMidi

import tree_class
from tree_class import forest

def _uartIn():
	pass

if __name__ == '__main__':
    data = tree_class.dataset_converter(dataset)
    tree_bases = tree_class.extract_tree_bases(dataset)
    
    chordForest = forest(tree_bases,data,\
                         word_to_ix,ix_to_chord)
    
    #test code below
    while True:
        #jetson only code##################################
        input_line = input("Input Number between 0-43: ")
        input_line = int(input_line)
	###################################################
        start_chord = tree_bases[input_line]
        chordForest.update_current_tree(start_chord)
    
        random_prog = chordForest.random_chord_progression()
        print(random_prog)
        listToMidi(random_prog,printOut=False)
