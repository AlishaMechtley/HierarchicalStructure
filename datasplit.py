##############################################
# Alisha Rossi
# 11/28/2011
# datasplit.py
#############################################

import os
import glob # supports unix code
resultfile = glob.glob('./*_run_*_f') # get the name of the file ending in _run_1_f
f = open (resultfile[0], 'r') # pointer, opens data file, still needs variable
f.seek(0) #finds the beginning of the file
h = f.readlines() #reads each line in the file 
start=h.index('Inferred ancestry of individuals:\n')+2 # finds the index of that line
i=start
clusters={} 
while h[i]!= '\n':
	column=h[i].split()
	if column[4]>column[5]:
		clusters[column[1]]=1
	else: 
		clusters[column[1]]=2
	i=i+1

#now each individual is associated with its cluster, and we extract the data

resultfile = glob.glob('./project_data*') # get the name of any file beginning with project_data
f = open (resultfile[0], 'r')

#create two subdirectories for the two populations
try:
	os.mkdir('cluster1')
	os.mkdir('cluster2')

except OSError:
	pass


# files to write to subdirectory
t1 = open('./cluster1/'+ resultfile[0]+'1', 'w') 
t2 = open('./cluster2/'+ resultfile[0]+'2', 'w') 
f.seek(0)
originaldata=f.readlines() 
t1.write(originaldata[0]) # put the first line into both files
t2.write(originaldata[0])
i=1
c1=0
c2=0
while originaldata[i]!= '\n': 
	cells=originaldata[i].split()
	if clusters[cells[0]]==1:
		t1.write(originaldata[i])
		c1=c1+1
	else:
		t2.write(originaldata[i])
		c2=c2+1
	i=i+1

t1.write('\n\n') # puts the two new lines at the end of each data file, same as original
t2.write('\n\n')
t1.close()
t2.close()

#The following function creates a parameter file for each new data file
def makespj(prjnm, n, numind):
	f = open('./cluster' + str(n) + "/" + prjnm+'.spj', 'w')
	f.write('PROJNAME  '+prjnm+'\n')
	f.write('NUMINDS  '+str(numind)+'\n')
	f.write('NUMLOCI  8\n')
	f.write('PLOIDY  2\n')
	f.write('MISSINGVAL  -9\n')
	f.write('ONEROW   0\n')
	f.write('INDLABEL   1\n')
	f.write('POPID   0\n')
	f.write('POPFLAG   0\n')
	f.write('LOCDATA   0\n')
	f.write('PHENOTYPE   0\n')
	f.write('EXTRACOL  0\n')
	f.write('MARKERNAME   1\n')
	f.write('RECESSIVEALLELE   0\n')
	f.write('MAPDISTANCE   0\n')
	f.write('PHASED   0\n')
	f.write('PHASEINFO   0\n')
	f.close()
	return 0

makespj('cluster1', 1, c1/2)

makespj('cluster2', 2, c2/2)

##########
#Notes###
#########
# copy this program and put into subfolder or find a way to run on subfolders
# remove "1" from project_data or use glob* to run again

#copy this program into subdirectory or
#go down a directory?
#subprocess.call("run structure here", shell=True)



