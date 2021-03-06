# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:49:51 2021

@author: james
"""

#Main File for Jetson Inference Package
from tree_imports import dataset
from tree_imports import word_to_ix
from tree_imports import ix_to_chord
from tree_imports import listToMidi

import tree_class
from tree_class import forest

def test(start_chord):
    chordForest.update_current_tree(start_chord)
    

if __name__ == '__main__':
    data = tree_class.dataset_converter(dataset)
    tree_bases = tree_class.extract_tree_bases(dataset)
    
    chordForest = forest(tree_bases,data,\
                         word_to_ix,ix_to_chord)
    
    #test code below
    start_chord = tree_bases[18]
    chordForest.update_current_tree(start_chord)
    
    random_prog = chordForest.random_chord_progression()
    print(random_prog)
    listToMidi(random_prog,printOut=False)