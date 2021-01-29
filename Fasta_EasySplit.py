#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,os
import argparse
import subprocess


print("Easy Fasta Splitter V2.0")
print("By: Patrick Gagne (patg97@hotmail.com)")

# Changelog
# 1. Remaining sequences are now divided between the containers instead of the last one
# 2. Main writing loop now use the file_index to determine the current container maximum size

parser=argparse.ArgumentParser(description='Split fasta into multipe files')

parser.add_argument("-f","--fas", dest="fasta_file", required=True, help=("Fasta file to split [REQUIRED]"))
parser.add_argument("-s","--split", dest="split_level", required=True,type=int, help=("Number of files to generate [REQUIRED]"))

args=parser.parse_args()

if args.split_level <= 1:
    print("ERROR: Split level must be greater than 1")
    sys.exit(1)

print("Counting sequences in %s"%(args.fasta_file))
pos_err=0

# Using posix commands to count sequence faster (using native unix commands grep and wc)
if os.name == "posix":
    print("POSIX system detected, POSIX command will be use to count sequence faster")
    try:
        count=int(subprocess.check_output("grep '>' %s | wc -l"%(args.fasta_file), shell=True).split()[0])
    except:
        pos_err=1
        print("Unexpected error on the posix command, reverting to standard python count")

# In case system is non posix (Windows for exemple) or if grep / wc command fail, use python commands (slower but safe)
if os.name != "posix" or pos_err==1:
    if pos_err == 0:
        print("Non POSIX system detected, Python will be used to count")
    count=0
    try:
        with open(args.fasta_file,"r") as infile:
            for line in infile:
                if line[0] == ">":
                    count+=1
    except IOError:
        print("ERROR: Fasta file %s not found or cannot be opened"%(args.fasta_file))
        sys.exit(1)

if args.split_level > count:
    print("ERROR: Split level (%i) greater then sequence count (%i)"%(args.split_level,count))
    print("Please reduce split level")
    sys.exit(1)


print("\nSequence count: %i"%(count))

# Calculating size for each container and calculating the remain sequences for the last file
container_size=int(count/args.split_level)
container_mod=count%args.split_level

# Creating list of size and splitting the renaming sequences between them (+1 sequence on some containers)
size_list=[container_size]*args.split_level
for i in range(container_mod):
    size_list[i]+=1


# If split level is a multiple of container_size, each container will be the same size
if container_mod > 0:
    print("Some files will contain %i sequences and some will contain %i sequences"%(container_size,container_size+1))
else:
    print("Each file will contain %i sequences\n"%(container_size))




# Open a serie of file which will contains the sequences and use a list to switch between them
file_list=[]
for i in range(1,args.split_level+1):
    file_list.append(open(args.fasta_file+"."+str(i),"w"))

seqnum=0
file_ind=0
with open(args.fasta_file,"r") as infile:
    for line in infile:
        # Case for the first sequence of the file (one time only)
        if seqnum == 0:
            print("Generating "+args.fasta_file+"."+str(file_ind+1))
            file_list[file_ind].write(line)
            seqnum+=1
            continue
        if line[0] == ">":
            # When you reach the current container size, switch to the next using the list index
            if seqnum+1>size_list[file_ind]:
                file_ind+=1
                seqnum=0
                print("Generating "+args.fasta_file+"."+str(file_ind+1))
                
            file_list[file_ind].write(line)
            seqnum+=1
        # For DNA lines, nothing to be done except dump them in the current file
        else:
            file_list[file_ind].write(line)
            
# Close all file in the list
print("Closing files")
for i in file_list:
    i.close()

print("\nFasta Splitting DONE\n")

