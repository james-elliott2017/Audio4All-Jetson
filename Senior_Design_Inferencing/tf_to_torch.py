# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:29:35 2021

@author: james
"""

#imports
import torch

data_file = r"tensor_essentialDataset.pt"
test_file = r"essential_torch.pt"
dataset = torch.load(data_file)

#torch.save(dataset,"essential_torch.pt")