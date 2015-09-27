# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:13:33 2015

@author: nausheenfatma
"""

import numpy as np
import random

class KMeansClustering:
	def __init__(self):
		self.array=None
		self.k=None
		self.k_centers=None
		self.cluster_dict=None
		self.previous_k_points=None
		self.new_k_points=None
		self.iteration_no=1
		self.no_of_iterations=10

  

	def initialise_array_from_file(self,file_path,kvalue,shape_tuple): 
		self.array=np.memmap(file_path, dtype='float32', mode='r', shape=shape_tuple) #binary memmap file
		self.k=kvalue


	def initialise_array_from_array(self,array,kvalue): 
		print "shape of array",array.shape
		self.array=array #binary memmap file
		self.k=kvalue  

	def set_no_of_iterations(self,no_of_iterations):
		self.no_of_iterations=no_of_iterations
    

	def run_kmeans_algo(self):

		self.k_centers=[]
		k_centers_points=self.random_initialise_cluster() #initialise cluster centroids
		print k_centers_points

		for i in k_centers_points:
			self.k_centers.append(self.array[i])

		self.k_means_cluster()

	def k_means_cluster(self):
		i=1
#		condition=None
#		if self.no_of_iterations==None:
#			condition=True
#		else :
#			condition= (i < self.no_of_iterations)

		while i < self.no_of_iterations:
		#while True: #repeat until convergence
			i=i+1
			previous_k_points=self.k_centers[:]
			self.find_clusters()
			self.update_centroids()
			new_k_points=self.k_centers	[:]	#copy by value
			v=np.array(previous_k_points) == np.array(new_k_points)
			if (v.all() == True) :
				print "Converged !!"
				print "no of iterations is : "+str(i)
				break
#			else :
#				print "Not Converged"
    

		
	def show_final_clusters(self):
			print "Final clusters : "
			for i in range(self.k):
				print str(i)+":"+str(self.cluster_dict[i])

	def find_clusters(self):
		self.cluster_dict={}
		if(self.iteration_no % 100==0):
			print "iteration no "+str(self.iteration_no)
		for i in range(self.k):
			self.cluster_dict[i]=[]

		for i in range(len(self.array)):
			cluster_no=0 
			min_dist=0
			for j in range(self.k): #find euclidean distance with each k means point
				dist=self.find_euclidean_distance(self.array[i],self.k_centers[j])
				if j == 0:
					min_dist=dist
				elif dist < min_dist :
					min_dist=dist
					cluster_no=j
			self.cluster_dict[cluster_no].append(i)
		self.iteration_no=self.iteration_no+1

	def update_centroids(self):
		column_size=self.array.shape[1]

		for i in range(self.k):
			sum=np.zeros(column_size)
			length=len(self.cluster_dict[i])
			for index in self.cluster_dict[i]:
				sum=np.add(sum,self.array[index])

			self.k_centers[i]=np.divide(sum,length)


	def random_initialise_cluster(self):	#random initialisation of k centroids
		no_of_rows=self.array.shape[0]
		d = [x for x in xrange(no_of_rows)]
		random_points=random.sample(d,self.k)
		return random_points


	def find_euclidean_distance(self,x1,x2):
		distance = np.linalg.norm(x1-x2)
		return distance

def main():
	km=KMeansClustering()
	shape_tuple=(9,4)	#feature vector size=4,no of instances=9
	km.initialise_array_from_file("/media/nausheenfatma/01CFC8995ADC9230/3rdSemester/NLP_TAship/WordRepresentation/WordRep/output/co_occ_file",3,shape_tuple) #k= no. of clusters
	km.set_no_of_iterations(10)
	km.run_kmeans_algo()
	km.show_final_clusters()

if __name__ == '__main__':
	main()

