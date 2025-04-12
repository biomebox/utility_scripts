#!/usr/bin/env python3

######### make a list of sseqid by Chandra Sarkar #########
# will concatenate all fasta files to one new fasta file
# will make a list of all the seqids/headers from the fasta files
## used to build the custom BLAST db

######### Importing required modules #########
import sys
import os
import inflect
from Bio import SeqIO
##############################################

### Get the current working directory ###
userInputDir = sys.argv[1] #user input of directory with ncbi downloads
currentDir = os.getcwd()
inputDir = os.path.join(currentDir, userInputDir) 

# Count subdirectories
subdirs = [entry for entry in os.scandir(inputDir) if entry.is_dir()]
countInFiles = len(subdirs)
p = inflect.engine()
countInTaxa = p.number_to_words(countInFiles)

### Set up output diretory ###
outDir = os.path.join(currentDir, f"fasta_files_{countInTaxa}")
if not os.path.exists(outDir):
    os.makedirs(outDir)

### open file to concatenate sequences ###
outFile = os.path.join(outDir,f"combined_{countInTaxa}.fasta")
writeOutFile = open(outFile, 'w')
all_records = []

### open file to count sequences ###
countFile = os.path.join(currentDir,f"sseqids_{countInTaxa}.csv")
writeCountFile = open(countFile, 'w')
writeCountFile.write("seqID,seq_length,name,info\n") # writing column names

### Get all the fasta files ###
for dirpath, dirnames, filenames in os.walk(inputDir):
    for file in filenames:
        if file.endswith('.fna') or file.endswith('.fas') or file.endswith('.fasta'):
            #print(file, filenames, dirpath)
            fastaFile = os.path.join(dirpath,file)
            recordsList = list(SeqIO.parse(fastaFile, 'fasta'))
            all_records.extend(recordsList)
            for readingFasta in SeqIO.parse(fastaFile, 'fasta'):
                header = readingFasta.description
                seqId = readingFasta.id # just the id
                seqLen = len(readingFasta.seq)
                writeCountFile.write("%s,%d,%s\n"%(seqId,seqLen,header))
writeCountFile.close()

### Write to a single merged FASTA file ###
SeqIO.write(all_records, writeOutFile, "fasta")
writeOutFile.close()
