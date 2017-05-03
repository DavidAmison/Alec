"""
Created on Fri Apr 28 16:05:30 2017

@author: David
"""

from textblob.classifiers import NaiveBayesClassifier
import os
from pathlib import Path

class classifier():
    
    def __init__(self,file):
        self.file_path = file
        file = open(str(file),'r')
        self.cl = NaiveBayesClassifier(file, format='csv')
        file.close()


    def classify_test(self,st):
        #Need to remove all commas from the string!
        st = st.replace(',','')
        result = self.cl.classify(st)
        prob = self.cl.prob_classify(st)
        print("the result is",result)
        print("Pos:{}, Neg:{}".format(prob.prob("pos"),prob.prob("neg")))
        expected = input("Is this correct (y/n)?")
        #Only update if certainty was less than 90% or we were wrong
        p = float(prob.prob(prob.max()))
        if expected == 'n':
            #update the train file and then update the classifier
            if result == "pos":
                #need to append as a negative result
                new_item = str(st+","+"neg")
                update = [(st,'neg')]
            else:
                new_item = str(st+","+"pos")
                update = [(st,'pos')]    
        else:
            new_item = str(st+","+result) 
            update = [(st,result)]
        
        if expected == 'n' or p < 0.9:
            file = open(str(self.file_path),'a')
            file.write(new_item+"\n")
            file.close()    
            self.cl.update(update)
        return
    
    def prob_classify(self,st):
        #Returns the probability distribution
        return self.cl.prob_classify(st)
    
    def classify(self,st):
        return self.cl.classify(st)