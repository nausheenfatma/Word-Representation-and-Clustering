from Unigram import Unigram
from Bigrams import Bigrams
from WordCoOccuranceMatrix import WordCoOccuranceMatrix
from K_means_clustering import KMeansClustering
import numpy
import ConfigParser

class Driver:
    def __init__(self):
        self.co_occ=None
        self.k=None
        self.input_path=None
        self.feature_vector_size=None
        self.no_of_words=0
        self.words=None
        self.output_path=None
        self.co_occ_path=None
        self.unigram_output_path=None
        self.bigram_output_path=None
        self.output_path=None
        self.no_of_iterations=None
        self.load_properties_file()
        
    def set_input_path(self,inputpath):
        self.input_path=inputpath        
        
    def set_output_path(self,outputpath):
        self.outputpath=outputpath        
        
    def set_parameters(self,k,f,no_of_iterations):
        self.k=k
        self.feature_vector_size=f
        self.no_of_iterations=no_of_iterations
        
        
    def find_unigrams(self):
        print "finding unigrams"
        print "inputpath",self.input_path
        u=Unigram()
        u.set_input_path(self.input_path)
        u.set_output_path(self.unigram_output_path)
        u.find_unigram()
        self.no_of_words=u.no_of_unigrams
        print "self.no_of_words",u.get_no_of_unigrams()
        self.words=u.ranked_list
        print "self.words",len(self.words)
        
        
    def find_bigrams(self):
        print "finding bigrams"
        b=Bigrams()
        b.set_input_path(self.input_path)
        b.set_output_path(self.bigram_output_path)
        b.find_bigrams()
        
    def find_cooccurance_matrix(self):
        print "finding cooccurance matrix"
        wcm=WordCoOccuranceMatrix()
        wcm.find_co_occurance_matrix()
        self.co_occ_file=self.co_occ_path


    def run_k_means(self):
    	print "running k means"
        print "k=",self.k
        print "self.co_occ_file",self.co_occ_file
    	km=KMeansClustering()
    	co_occ = numpy.memmap(self.co_occ_file, dtype = 'float32', mode = 'r',shape=(self.no_of_words,self.feature_vector_size))
    	km.initialise_array_from_array(co_occ,self.k)
        km.set_no_of_iterations(self.no_of_iterations)
    	km.run_kmeans_algo()
       # print "self.words",self.words
        print "Final clusters :"
        for i in range(km.k):
            print str(i)+":"+str(km.cluster_dict[i])
            words_in_cluster=[]
            for index in km.cluster_dict[i]:
                words_in_cluster.append(self.words[index][0])
            print words_in_cluster
            
            
    def load_properties_file(self):
        config = ConfigParser.RawConfigParser()
        config.read('Config.properties')
        self.output_path=config.get('OutputPathSection','output_path')
        self.co_occ_path=self.output_path+config.get('OutputPathSection','co_occ_file_name')
        self.unigram_output_path=self.output_path+config.get('OutputPathSection','unigram_file_name')
        self.bigram_output_path=self.output_path+config.get('OutputPathSection','bigrams_file_name')
        self.k=config.get('DefaultParameters','k')
        self.feature_vector_size=config.get('DefaultParameters','f')
        self.no_of_iterations=int(config.get('DefaultParameters','iterations'))
    
    def run(self):
        self.find_unigrams()
        self.find_bigrams()
        self.find_cooccurance_matrix() 
        self.run_k_means()
        
    
def main():
    driver =Driver()
    driver.set_input_path("/../input/English_sample.txt")
    driver.set_parameters(k=5,f=5,no_of_iterations=10)
    driver.run()

if __name__ == '__main__':
	main()
