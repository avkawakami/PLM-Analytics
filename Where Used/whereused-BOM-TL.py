#!/usr/bin/env python3
#Program to compile the where-used list based on BOM
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:13:20 2017

@author: andrekawakami

MIT License

Copyright (c) 2022 avkawakami
"""

# This script uses as input a csv file called BOM.csv
# The structure of the fie is:
#Parent;Child


import csv
import time
import json
tic = time.time()

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


reader = csv.reader(open('BOM.csv','rU'), delimiter=';')


# Define the list of top level assemblies. 
# Assumptions are that
# 1st character of top level assembly is a "A"
# 8th character of top level assembly is a "B" 

TopLevel = {}
counterTL = 0
for par, chi in reader:

    if str(par)[:1] == 'A' and str(par)[8:9] == 'B': #if needed customize your top level assembly here
        counterTL = counterTL + 1
        TopLevel.setdefault(par, []).append(chi)

reader = csv.reader(open('BOM.csv','rU'), delimiter=';')

# Define the structure list

structure = {}
for par2, chi2 in reader:
    if str(par)[:1] != 'A' and str(par)[8:9] != 'B': #if needed customize your top level assembly here
        structure.setdefault(par2, []).append(chi2)

whereused = TopLevel     


# includes the structure items on the respective top level
for par3, chi3 in whereused.items():    
    for value in chi3:
        if value in structure.keys():
            if len(structure[value]) == 1:
                whereused[par3].append(str(structure[value]).strip("[']"))
            if len(structure[value]) != 1:
                for items in structure[value]:
                    whereused[par3].append(items.split('\t')[0])
    whereused[par3] = remove_duplicates(whereused[par3])

# Stores the top level usage as json for future reference

with open('top-level-structure.json', 'w') as f:
    json.dump(whereused, f)
toc =  time.time()

print('It took ', toc-tic, ' seconds for running this script')
print (counterTL)
