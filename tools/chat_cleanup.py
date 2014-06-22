#!/usr/bin/python

from collections import OrderedDict
import sys, os

if len(sys.argv) < 3:
    print('Usage: %s chatlist_in.dat chatlist_out.dat' % sys.argv[0])
    sys.exit(1) 

inFile = sys.argv[1]
outFile = sys.argv[2]

with open(inFile, 'r') as file:
    words = file.readlines()
 
words = [word.rstrip('\n') for word in words]
 
for index, word in enumerate(words):
    try: words[index] = int(word)
    except: pass
 
sorted_words = list(OrderedDict.fromkeys(sorted(words)))
 
with open(outFile, 'w+') as file:
    for word in sorted_words:
        file.write(str(word) + '\n')
 
print "A total of %d duplicates were removed." % (len(words)-len(sorted_words))
print "A total of %d words were sorted." % len(sorted_words)
