import os
import sys
from collections import OrderedDict
import glob
import ntpath
import ruamel.yaml as yaml
import codecs
import pdb

if (len(sys.argv) is not 3):
    print ("Error: Need <input folder> followed by <output folder>")
    exit()

inputFolder = sys.argv[1] # first argument: input folder
outputFolder = sys.argv[2] # second argument: output folder

listInputFiles = glob.glob(os.path.join(os.getcwd(), inputFolder, "**", "*.yaml"), recursive = True)
print (str(len(listInputFiles)) + " input files found..")

urduOutputContents = []
romanOutputContents = []


for inputFilename in listInputFiles[0:2]:
    with open(inputFilename, 'r') as inputFile:
      fileContents = inputFile.read()

      print ("Processing file: " + ntpath.basename(inputFilename))

      yamlObject = yaml.load(fileContents, Loader=yaml.Loader)
      shers = yamlObject['sher']
      for sher in shers:
          urduSher = [i['text'] for i in sher['sherContent'] if i['lang'] == 'ur'][0]
          urduLines = [line.strip() for line in urduSher.split("|")]

          romanSher = [i['text'] for i in sher['sherContent'] if i['lang'] == 'ro'][0]
          romanLines = [line.strip() for line in romanSher.split("|")]

          if len(urduLines) is not len(romanLines):
            print ("Error: lines mismatch")

          for index in range(len(urduLines)):
            urduOutputContents.append(urduLines[index])
            romanOutputContents.append(romanLines[index])

# Create output folder if it does not exist
absOutputFolderPath = os.path.join(os.path.join(os.getcwd(), outputFolder))
if not os.path.exists(absOutputFolderPath):
    os.makedirs(absOutputFolderPath)

# Dump urdu and roman data in 2 different files in the output folder given by user

urduOutputFilePath = os.path.join(absOutputFolderPath, "complete-urdu-books.ur")
romanOutputFilePath = os.path.join(absOutputFolderPath, "complete-urdu-books.ro")

with open(urduOutputFilePath, 'w') as outputFile:
    outputFile.write("\n".join(urduOutputContents))

with open(romanOutputFilePath, 'w') as outputFile:
    outputFile.write("\n".join(romanOutputContents))
