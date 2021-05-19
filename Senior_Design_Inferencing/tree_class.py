# -*- coding: utf-8 -*-
"""
Created on Tue May  4 12:30:52 2021

@author: james
"""
import numpy as np
import copy
import random

def decoder(ix_to_chord,code=0):
  """
  code: input encrypted recommendation from model
  """
  string = ix_to_chord[code]
  string = string.replace("["," ")
  string = string.replace("]"," ")
  string = list(string.split(" "))
  final_chord = [int(x) for x in string if x != ""]
  return final_chord
########################################################################
####Tree Creator & Updater Code############
###STEP 1: Dataset Eval
def dataset_converter(dataset):
    data = copy.copy(dataset)
    data = data.numpy()
    data = np.ndarray.tolist(data)
    return data

###STEP 2: Independent Tree Starting Points
def extract_tree_bases(dataset):
    tree_bases = []
    #loop through first chord in each progression
    for chord in dataset[:,0,:]:
      start_chord = chord.numpy()
      if tree_bases != []:
        ##check if chord already exists##
        does_exist = False
        for existing_chord in tree_bases:
          if (existing_chord == start_chord).all():
            does_exist = True
        if does_exist == False:
          tree_bases.append(list(start_chord))
      #first pass
      else:
        #first pass
        tree_bases.append(list(start_chord))
    return tree_bases
#######################################################################
#CLASS INITIALIZATION
class tree:
  def __init__(self,first_chord,data):
    self.tree_base = first_chord
    #added in response to inferencing. If issues, please remove
    self.data = data

    self.layer1 = self._layer_creator(data,layer_index=1)
    self.layer2 = self._layer_creator(data,layer_index=2)

  def updateTree(self,first_chord):
    self.tree_base = first_chord
    self.layer1 = self._layer_creator(self.data,layer_index=1)
    self.layer2 = self._layer_creator(self.data,layer_index=2)

  def _treelocations(self,dataset,tree_base):
    root_idxs = []
    for i, prog in enumerate(dataset):
      if prog[0] == tree_base:
        root_idxs.append(i)
    return root_idxs

  def _layer_creator(self,dataset,layer_index):
    root_idxs = self._treelocations(dataset,tree_base=self.tree_base)

    layer_dict = {}
    #create non_duplicate chords for layer
    for ix in root_idxs:
      #grab chord for that layer
      current_chord = dataset[ix][layer_index]
      next_chord = dataset[ix][layer_index+1]
      if str(current_chord) not in layer_dict.keys():
        layer_dict[str(current_chord)] = []
        layer_dict[str(current_chord)].append(next_chord)
      elif next_chord not in layer_dict[str(current_chord)]:
        layer_dict[str(current_chord)].append(next_chord)
      else:
        continue
    return layer_dict

  def printInfo(self):
    print("tree_base: {}\nlayer_1 dictionary:\n{}\nlayer_2 dictionary:\n{}".format(self.tree_base,self.layer1,self.layer2))

###############################################################################################################################
class forest:
  def __init__(self,first_chord_list,data,word_to_ix,ix_to_chord):
    self.word_to_ix = word_to_ix
    self.ix_to_chord = ix_to_chord
      
    self.first_chord_list = first_chord_list
    self.dataset = data
    self.current_root = []

    #initialize sub-instance for single tree for class protection
    self.current_tree = tree(self.first_chord_list[0],self.dataset)
  
  def update_current_tree(self,start_chord):
    """
    update current tree from start_chord_location
    """
    if start_chord != self.current_root:
      if start_chord in self.first_chord_list:
        self.current_root = start_chord
        self.current_tree.updateTree(self.current_root)
      else:
        print("chord not found in dataset")
    else:
      print("Tree Already Loaded")
  
  def _random_key_selector(self,dictionary):
    """
    returns a random key from a dictionary
    """
    key_choice = random.choice(list(dictionary.keys()))
    return key_choice

  def random_chord_progression(self):
    def _str_check(final_prog):
      x = final_prog
      for idx, chord in enumerate(x):
        if type(chord) == type("s"):
          input = chord.replace(",","")
          encoded = self.word_to_ix[input]
          decoded = decoder(self.ix_to_chord,code=encoded)
          x[idx] = decoded
      return x
    #chord_1
    chord_1 = self.current_root
    # print("1: ",chord_1)

    #chord_2
    chord_2 = self._random_key_selector(self.current_tree.layer1)
    # print("2: ",list(chord_2))

    #chord 3
    chord_3 = random.choice(self.current_tree.layer1[str(chord_2)])
    # print("3: ",chord_3)

    #chord 4
    chord_4 = random.choice(self.current_tree.layer2[str(chord_3)])
    # print("4: ",chord_4)

    final_prog = []
    final_prog.append(chord_1)
    final_prog.append(chord_2)
    final_prog.append(chord_3)
    final_prog.append(chord_4)

    final_prog = _str_check(final_prog)
    return final_prog

