# -*- coding: utf-8 -*-
"""
rnn.py - recurrent neural network


:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class BGRUV(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes,
                 **kwargs):
        super(BGRUV, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.bgru = nn.GRU(
            input_size, hidden_size, num_layers, bidirectional=True, **kwargs)
        self.dense = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes),
            nn.Softmax()
            )

        def forward(self, x):
            packed_x = 
