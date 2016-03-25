Heirarchical Analysis of Population Data Using a Recursive Implementation of Structure Software
===============================================================================================

## Introduction

The Structure program uses a model-based clustering method for inferring population structure using genotype data consisting of unlinked markers. The software can be used to demonstrate the presence of population structure, to assign individuals to K populations (where K may be unknown), and to identify migrants and admixed individuals.  The goal of my project was to recursively run the Structure program with k=2 populations and analyze the topology of the resulting tree. The method works as as follows: I run structure with k=2 clusters, separate the data into two files using Q values (discussed later), create a parameter file for each data subset and repeat the process until I get Q values of one over the value of k (both populations equally likely).
Why Structure? The Structure program uses a Bayesian model. Bayesian inference provides consistent and efficient parameter estimates under general conditions. This is similar to maximum likelihood inference but the result is a prior probability distribution instead of point estimates. The posterior distribution is given by the following equation:

Where X is a vector of the observed allele copies of each individual, Z is a vector of the unknown populations of origin of each allele copy, and P is unknown allele frequencies in all populations. The posterior distribution is estimated using a MCMC algorithm described as follows:

1.	Step 1: Estimate the allele frequencies for each population and the admixture proportions of each individual assuming that the population of origin of each allele copy in each individual is known (i.e., sample P). 

2.	Step2: Estimate the population of origin of each allele copy assuming that the population allele frequencies and the admixture proportions are known (i.e., sample Z).

3.	Step 3: A Metropolis-Hastings update to integrate out the uncertainty of alpha.

The model assumes Hardy-Weinberg equilibrium and linkage equilibrium between loci. In other words, each allele at each locus in each genotype is an independent draw from the appropriate frequency distribution. The program allows for some admixed individuals by using a vector called Q. The proportion of that individual’s ancestry from each population, Q, has a Dirchlet distribution with a parameter called alpha (used in Step 3 above). The alpha parameter is one of two default values that structure prints out; the other is the fixation index (Fst).
Prichard, Stephens, and Donelly (2000) discuss alpha as being in the interval [1,10]. Large numbers of alpha (>>1) model each individual as having allele copies originating from all K populations in equal proportions. Small values of alpha (<<1) models each individual as originating from mostly a single population. Alpha is uniformly chosen at random and updated at each step. The Fst cmay be considered as indicating little (0 to 0.05), moderate (0.05 to 0.15), great (0.15 to 0.25), or very great (>0.25) genetic differentiation.
The values of alpha and Fst should converge. I began with a small fish dataset (Robusta) and noticed that these values did not converge to a single number, but this may be due to how small the sample is. I tried varying the burnin lengths but it still did not converge until I increased the Metropolis-Hastings update step (the standard deviation of the proposal for alpha) to improve mixing.

## Modelling Decisions

Prichard, Stephens, and Donelly (2000) use a burnin length of 30,000 and a run length of 10^6 on a sample fish dataset called Robusta. I used this as a starting point on my sample dataset and some of the results are shown below.


| Run  | Burn-in length |	MCMC reps	|    alpha 	    |    Fst 1	  |   Fst 2	    | Clustered Groups 1 |	Clustered Groups 2  |
| ---- |:--------------:|:-------------:|:-------------:|:-----------:|:-----------:|:------------------:|:--------------------:|
| A	   | 50,000	        | 50,000	    | 0.0146	    | 0.0146 	  | 0.2926      | 1,3,4,5,7,8,9	     | 2,6                  | 
| B	   | 50,000	        | 1,000,000	    | 0.0269	    | 0.0196	  | 0.605	    | 1,3,4,5,6,7,8,9	 | 2                    |
| C	   | 100,000	    | 1,000,000	    | 0.0289	    | 0.0165	  | 0.2924	    | 1,3,4,5,7,8,9	     | 2,6                  |


For most runs, I got similar results to run A and C above. Occasionally I got conflicting results (like in run B). I kept clustering until the Q values started to look like they are at 50% for each cluster for ever individual. For example, when I try to cluster the individuals in bol1- bol30 I get results like this:
```
Label	(%Miss)	Inferred	clusters	
1	bol1	:	0.490	0.510
2	bol2	:	0.501	0.499
3	bol3	:	0.492	0.508
.
.
.
```
So at this point, I stopped trying to cluster the group any further. I kept running each cluster in structure until I got results similar to what you see above. I figure that's a good place to stop when there is an equaly likely probability to fall in either group.

## Results

Robusta Data

The following diagram shows the results (by location) for Run A.
 ![Figure 1](https://raw.githubusercontent.com/AlishaMechtley/HierarchicalStructure/master/images/img1.png)

This next tree shows the individuals in each cluster:

 ![Figure 2](https://raw.githubusercontent.com/AlishaMechtley/HierarchicalStructure/master/images/img2.png)


I would like to run this data again on k=4 and see if populations 2, 6, 3 with 9, and the rest cluster out separately. I would also like to know the background information of the dataset (at what locations were the fish samples taken? What are the different types of fish?). I was unable to find a dataset with this kind of information.

## Thrush Data

I ran the 155 individuals of the Kenyan thrush ( T. helleri) dataset (Pritchard et. al, 2000) that were collected in three separate refugia of indigenous cloud forest. All I could really look at is whether the number of tips in the tree that I created was the same as the optimal k-value that was suggested in the paper, and indeed it was. Here are the individuals that clustered at the tips:

```
Cluster 1 
PopID = 2 unless otherwise specified (Mbololo?)
1, 10, 1219, 1225, 1244, 1254, 1274, 1284, 1297, 1302, 1317, 1319, 1326, 1327, 1328, 2, 5, 29, 30, 31, 32, 45, 58, 59, 62, 63, 68, 8, 980, 981, 984, 987, 988 
989, 990, 994,1226, 1228, 1238, 1243, 1253, 1275, 1277, 1296, 1299, 1303, 1304, 1312, 1318, 1320, 1321, 1323, 1324, 1325, 16, 21, 33, 34 (3), 37, 4, 46, 47, 55, 56, 57, 60, 64, 66, 67, 69, 978, 979, 982, 983, 985, 986, 991, 992, 993, 1223, 1322

Cluster 2.1 
PopID = 1 unless otherwise specified (Chawia?)
9, 20, 27, 36 (3), 42 (3), 429, 457, 471, 479, 494, 505, 508, 604, 691, 715, 755 (4), 894, 952, 956, 1329

Cluster 2.2 
PopID = 3 unless otherwise specified (Ngango?)
15, 17, 19, 28, 38, 40, 41, 43, 44, 48, 49, 50, 51, 52, 54, 61, 7, 724 (4), 768 (4), 806 (4), 817, 827, 828, 829, 834, 845, 846, 853, 864, 865, 877, 884, 886, 890, 901, 911, 915, 918, 920, 921, 928, 929, 933, 937, 951, 957, 966, 967, 968, 969, 970, 974, 975, 976 
```

I clustered the data into two groups. On the second cluster I ran structure again and got two more clusters. Generally, the data clustered into the same populations as specified by the population ID (PopID). It would be interesting to see if these clusters match the clusters from the paper. Unfortunately, the data does not indicate which individuals came from which sample location (Chawia, Mbololo, Ngangao) so I can only speculate. I decided to run the program with k=3 and see if the results are the same as the results from a single run with 3 clusters. I also compared my triangle plot (for k=3) to the plot from the paper.



 ![Figure 3](https://raw.githubusercontent.com/AlishaMechtley/HierarchicalStructure/master/images/img3.png)

 ![Figure 4](https://raw.githubusercontent.com/AlishaMechtley/HierarchicalStructure/master/images/img4.png)


The triangle plot of vector Q on the left is from Pritchard, et al. 2000. The triangle on the right is a single k=3 run with both burn-in and number of MCMC reps set to 100,000.  Each of the three vector components of Q is plotted as a distance to one edge of the triangle. A colored point represents each individual. The points correspond to the prior population labels. As you can see, the two plots look somewhat similar. 

I painstakingly checked which group each individual clustered to and I shaded accordingly in the box below. It’s important to note that the colors are not exactly the same as those in the triangle for a reason. This is because I am showing the resulting clusters and not the prior population labels (as the triangle shows). The italicized individuals clustered together, the bold clustered together, and the plain text clustered together. 

## Cluster 1 PopID = 2 unless otherwise specified (Mbololo?)

*1, 10, 1219, 1225, 1244, 1254, 1274, 1284, 1297, 1302, 1317, 1319, 1326, 1327, 1328, 1226, 1228, 1238, 1243, 1253, 1275, 1277, 1296, 1299, 1303, 1304, 1312, 1318, 1320, 1321, 1323, 1324, 1325* 

#### 2, 5, 29, 30, 31, 32, 45, 58, 59, 62, 63, 68, 8, 980, 981, 984, 987, 988, 989, 990, 994, 16, 21, 33, 34, 37, 4, 46, 47, 55, 56, 57, 60, 64, 66, 67, 69, 978, 979, 982, 983, 985, 986, 991, 992, 993, 1223, 1322

## Cluster 2.1 PopID = 1 unless otherwise specified (Chawia?)

9, 20, 27, 36, 42, 429, 457, 471, 479, 494, 505, 508, 604, 691, 715, 755, 894, 952, 956, 1329

## Cluster 2.2 PopID = 3 unless otherwise specified (Ngango?)

#### 15, 17, 19, 28, 38, 40, 41, 43, 44, 48, 49, 50, 51, 52, 54, 61, 7, 724, 768, 806, 817, 827, 828, 829, 834, 845, 846, 853, 864, 865, 877, 884, 886, 890, 901, 911, 915, 918, 920, 921, 928, 929, 933, 937, 957, 966, 967, 968, 969, 970, 974, 975, 976 

*951*

As you can see, my results do not match the k=3 run, especially for PopID=2, but my results match the preliminary population information (PopID) better. Excluding the 4 individuals that have PopID=4, 98% of the individuals clustered to the same group as their PopID in the recursive runs whereas only 70% clustered to the same groups as their PopID for the single k=3 run. This could be because there is a lot of variation in the data (especially where PopID = 2) and some of this is lost when the data is separated. 
Perhaps the PopID has more “weight” in deciding where to cluster individuals when there is less information (when I run structure recursively). To check this, I decided to see what would happen if I changed the PopID to be the number of the cluster (from the single k=3 run). I first used the original PopID numbers as location information and redid the runs. I also tried removing the original preliminary population numbers completely and simply replacing them with the cluster numbers. In both cases, I get the same results as before for a (burnin = 100,000 and number of MCMC Reps  = 100,000). Thus, it appears that the PopID does not seem to have much of an influence on the result of the clustering.  

## Adult Fish Data

In addition to the Robusta data, I also did several runs for another fish dataset (unpublished data from a doctoral student). The resulting Q values all bordered 0.500 and so there is not enough variation in the data to use this recursive method.

## Simulations

Using Migrate-n, I simulated 3 populations with 10 loci. I sampled 10 individuals from a population of 100 for all three cases (see infile and parmfile for details).  When I ran Structure with k=3 and 100,000 for the burnin and MCMC reps, The 30 individuals were clustered into the three correct populations. I ran the program again with k=2. One group was clustered separately from the other two and the other two were separated in a subsequent run with k=2. Thus, the final number of clusters in the end was the same and the clusters were correct in both cases. I would like to do more runs with varying parameters (mutation, migration rate, sample size, and population size). 

## Future Work

To compare these results to other tree building methods, I am considering taking the top of a tree produced by a tree building algorithm and collapsing the tips into the ancestor nodes. To look at the accuracy of the method, I need to simulate data in a way that saves the order of divergences so that I know the true topology of the simulated data. I would also like to automate this process better. I tried calling structure from the command line and couldn’t get it to work. Once I get this to work, I can call Structure from within python on each cluster I create.
