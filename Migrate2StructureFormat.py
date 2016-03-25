#######################################
# Alisha Rossi
# 12/1/2011
# Migrate2StructureFormat.py
# writes migrate file to file in structure format.
# Remove the migrate file line starting with "#" if it exists
# Note that Structure only takes integers for missing data (ex, -9)
#######################################

import sys
import os
import glob # supports unix code
resultfile = glob.glob('./*.txt') 

#######################################
#read in file
#######################################
try:
	filename = sys.argv[1]
except:
	filename=resultfile[0]					# if no file given, use first txt file found in directory

with open(filename) as f:					# automatically closes input file as soon as it's done
	fileData=f.readlines()

########################################
# renaming and row-splitting function
########################################								
#split the first row by space
delimiter = '.'
counter = 0 
#f.seek(0) #finds the beginning of the file?
firstline=fileData.pop(0) #pop the first item in the list instead of the last
a=firstline.split('(')						# take first part of first line
siteNames = a[1].rstrip(')\n')				# remove parenthesis on second part
popNum = int((a[0].split(' '))[0]) 			# get first number by splitting

fout= open('project_data', 'w')				#Structure File to be written
fout.write(siteNames+ '\n')


for line in fileData:
	a=line.split()
	if len(a)==2:
		popName = a[1]						# create unique row names, for every row with two columns
		counter = 0							
	else:
		
		alleles=[pair.split('.') for pair in a[1:]] # list comprehension, each alleles element is a two element list
		allele1=[pair[0] for pair in alleles]		# list of first of each pair
		allele2=[pair[1] for pair in alleles]		# list of second of each pair	
		indivName=popName+str(counter)
		indivName = indivName.ljust(11, ' ') 		# left adjust identifier a[0] and make it 10 characters using underscores

		fout.write(indivName + ' '.join(allele1) + '\n') #joins each allele loci with a space
		fout.write(indivName + ' '.join(allele2) + '\n')
		counter=counter+1

fout.close()




