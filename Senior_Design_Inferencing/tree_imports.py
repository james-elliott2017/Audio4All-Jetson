"""
Created on Tue May  4 11:34:47 2021

@author: james
"""

#imports
import torch

from mido import Message, MidiFile, MidiTrack

#from random import randint
#import random
#import copy
import os
import pickle
#print("Imports Complete")

data_file = r"tensor_essentialDataset.pt"
dataset = torch.load(data_file)
#print(dataset.shape)


#functions
def listToMidi(chord_list,
               dir_path = 'midi_out/',
               file_name = "new_song.mid",
               program = 12,
               dt = 256,
               veloON = 64,
               veloOFF = 127,
               printOut = True,
               saveMidiFile=True,
               completePath = False):
  """
  converts midi value chords into a midi file with given specifications.
  """
  mid = MidiFile()
  track = MidiTrack()
  mid.tracks.append(track)

  #initialize instrument type
  track.append(Message('program_change', program=12, time=0))
  #Loop through each all chords in list
  for chord in chord_list:
    start = True
    
    #turn chord(s) on
    for note in chord:
      if start == True:
        
        track.append(Message('note_on', note=note, velocity=veloON, time=dt))
        start = False
      else:
        track.append(Message('note_on', note=note, velocity=veloON, time=0))

    start = True
    #turn chord(s) off
    for note in chord:
      if start == True:
        track.append(Message('note_off', note=note, velocity=veloOFF, time=dt))
        start = False
      else:
        track.append(Message('note_off', note=note, velocity=veloOFF, time=0))

  #print created track
  if printOut == True:
    for msg in mid:
      print(msg)
  
  #save midi file
  if saveMidiFile == True and completePath == False:
    complete_path = os.path.join(dir_path,file_name)
    #print(complete_path)
    mid.save(complete_path)
    print("\nfile saved @\n{}".format(complete_path))
  elif completePath != False:
    mid.save(completePath)
##########################################################
##########################################################
#NOT WORKING RIGHT NOW
def midiExtend(file_path,dupNum=2,save_path = False):
  mid = MidiFile(file_path)

  final_tracks = MidiTrack()
  for i in range(dupNum):
    for track in mid:
      #print(track)
      final_tracks.append(track)

  #create new file name
  file_name = "midi_extended"
  num = str(dupNum)
  extension = ".mid"
  full_name = file_name + num + extension

  path = "/".join(file_path.split("/")[0:-1])
  #print("Path {}\n".format(path))
  #print(full_name)
  mid_final = MidiFile()
  mid_final.tracks.append(final_tracks)
  
  final_path = os.path.join(path,full_name)
  mid_final.save(final_path)
#########################################################################
#########################################################################
def datasetEmbedder(dataset,inputLength=3):
  """
  dataset: tensorflow dataset with dimensions (total_progs,progression length,notes in chord)
  inputLength: # of chords played.

  Function seperates progressions into "input" & "target"
  """
  assert len(dataset[0]) > inputLength, "inputLength needs to be less than progression length"
  #quadgrams = [(progression[:3],progression[3]) for progression in dataset]
  if inputLength != len(dataset[0]):
    grams = [(progression[:inputLength],progression[inputLength]) for progression in dataset]
  
  return grams

def decoder(code=0):
  """
  code: input encrypted recommendation from model
  """
  string = ix_to_chord[code]
  string = string.replace("["," ")
  string = string.replace("]"," ")
  string = list(string.split(" "))
  final_chord = [int(x) for x in string if x != ""]
  return final_chord

#######################Lookup Table Functions###################################
def createLookup(dataset):
  #create chords as a singular word
  vocab = []
  for prog in dataset:
    for chord in prog:
      tmp_chord = str(chord.numpy()) #convert chord to string
      vocab.append(tmp_chord)
  vocab = set(vocab)
  print("# of Chords in Vocab: {}".format(len(vocab)))

  #create lookup table
  word_to_ix = {word:i for i,word in enumerate(vocab)} #encode
  ix_to_chord = {i:word for i,word in enumerate(vocab)} #decode

  return vocab, word_to_ix, ix_to_chord

def saveLookUp(encode_dict,decode_dict,dirPath):
  """
  encode: word_to_ix
  decode: ix_to_chord
  """
  file_encode = r"lookUp_encode.txt"
  file_decode = r"lookUp_decode.txt"
  #save files
  with open(os.path.join(dirPath,file_encode), "wb") as myFile_encode:
    pickle.dump(encode_dict, myFile_encode)

  with open(os.path.join(dirPath,file_decode), "wb") as myFile_decode:
    pickle.dump(decode_dict, myFile_decode)

  print("Files Saved @:\n{}".format(dirPath))

def loadLookUp(dirPath):
  """
  reverse of saveLookUp()
  """
  file_encode = r"lookUp_encode.txt"
  file_decode = r"lookUp_decode.txt"

  with open(os.path.join(dirPath,file_encode), "rb") as myFile_encode:
    encode_dict = pickle.load(myFile_encode)

  with open(os.path.join(dirPath,file_decode), "rb") as myFile_decode:
    decode_dict = pickle.load(myFile_decode)

  assert len(encode_dict) == len(decode_dict), "encode and decode must be same length"

  vocab = encode_dict #used for the len(vocab) for embed dimensions

  return encode_dict, decode_dict, vocab
########################################################################
########################################################################
#encoder,decoder intialization
lookup_table_path = r"lookup_tables"
word_to_ix, ix_to_chord,vocab = loadLookUp(lookup_table_path)
