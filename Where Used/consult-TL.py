#!/usr/bin/env python3
#Program to read a list of items and identify the top level assemblies
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:04:26 2017
MIT License

Copyright (c) 2022 avkawakami

"""


import json
import csv
import time

tic = time.time()
# Opens the top-level-structure.json file, previous compiled using the whereused-BOM-TL.py

with open('top-level-structure.json') as f:
    whereused = json.load(f)


# Loads the list of affected items from affectedpns.txt
affected = [line.rstrip('\n') for line in open('affectedpns.txt')]

usage = []     
results = []
i = 0
# Creates a results file where the top level will be identified

with open('results-TL.csv', "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    for PN in affected:
        for par, chi in whereused.items():
            for value in chi:
                if value == PN:
                     writer.writerow([PN, par])
        i = i + 1

toc = time.time()

print ("Concluded!!! It saved " , toc-tic, " seconds from your life, instead of ", i / 2, "minutes!!")
print ("Check the results-TL.csv with your results")