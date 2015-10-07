# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 13:01:49 2015

@author: lauren
"""

#This function will take in a dataframe of triathlon results and generate a graph where nodes are individuals 
#(as identified by Firstname, Lastname, Yearborn) and nodes are connected by weighted edges with weights 
#given by the number of races in which individuals have both competed.

import networkx as nx

G = nx.Graph()