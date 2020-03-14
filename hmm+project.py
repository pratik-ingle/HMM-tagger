
# coding: utf-8

# In[330]:

import nltk 
from nltk.corpus import brown
import collections
import numpy as np
import pandas as pd


# In[331]:

# frequency function 
def fre(x):
    from collections import Counter
    types =  Counter(tuple(x) for x in x )
    #print(types)  # types is in the form of directories

    # converting dictionary into two dimentional array 
    freq = []
    for value in types.items() :
        freq.append(value)

    #sorting array  in decending order
    def sortthird(freq): 
        return freq[1] 
    freq.sort(key = sortthird ,reverse = True) 
    #print(freq)
    return freq


# In[ ]:




# In[332]:

# insert start "<s>" and end "<\s>" symbols for each sentence 
p = brown.tagged_sents()
brown_corpus = []
for i in p :
    i.insert(0,('<s>','<s>'))
    i.insert(len(i),('<\s>','<\s>'))
    brown_corpus.append(i)
    
# creating test and training sets from brown corpus
#test set containt first 100 sentences for testing porpuse
brown_test = []
brown_train = []
sen = 0
for i in brown_corpus:
    sen += 1
    if sen <= 10:
        brown_test.append(i)
    else:
        brown_train.append(i)
        
#considering training set as only [word , tag] insted of sentence 
brown_words_tag = []
for i in brown_train:
    for j in i:
        brown_words_tag.append(j)
        
# frequency of brown_words_tag
fre_wordtag = fre(brown_words_tag)
#print(fre_wordtag)

#frerquency of ti (tag) 
brown_tag = []
for i in brown_train:
    for j in i:
         brown_tag.append(j[1])

# getting frequency of brown_tag
types =  collections.Counter(brown_tag)
#print(types)  # types is in the form of directories

# converting dictionary into two dimentional array "a"
fre_tag = []
for value in types.items() :
    fre_tag.append(value)

#sorting array in decending order
def sortthird(fre_tag): 
    return fre_tag[1] 
fre_tag.sort(key = sortthird ,reverse = True) 
#print(fre_tag)


# In[334]:

# probabitity of p(wi|ti)
probWiti = []
list1 =[]
list2 = []
list3 = []
for i in fre_wordtag:
    for j in fre_tag:
        if i[0][1] == j[0]:
            temp = [i[0] , i[1]/j[1]]
            probWiti.append(temp)
            list1.append(i[0][0])
            temp1 = [i[0][1], i[1]/j[1]]
            list2.append(temp1)

#probWiti

#probability of p{ti|t(i-1)}

#frequency of bigram taggs
bi_tag = []
x = len(brown_words_tag)
for j in range(x):
    if j+1 < x:  
        temp = [brown_words_tag[j][1] , brown_words_tag[j+1][1]]
        if temp != ['<\s>' ,'<s>' ]: # not cosidering ['<\s>' ,'<s>'] count b/z it's a end of sentance 
            bi_tag.append(temp)

# frequency of 
fre_bi_tag= fre(bi_tag)
#print(fre_bi_tag)

# probabitity of p(wi|ti)
probbitag = []
for i in fre_bi_tag:
    for j in fre_tag:
        if i[0][0] == j[0]:
            temp = [i[0] , i[1]/j[1]]
            probbitag.append(temp)

#probbitag

# set of all differet tags present in brown corpus
#since the probability of word depending on tag and probability of tag depeds on its previous tag there should not be any unk tag present
# in HMM tagger
pos_tag = [] 
for i in fre_tag:
    pos_tag.append(i[0])


# In[ ]:




# In[336]:

# vitervi algorithm

# creating lattice of transition and emissions probability
for j in probWiti:
    j[0][0]
        
      

#emission probability for this sentance
l = len(sentance)
c = 1
sentance = brown_test[4]    # change the sentance by replacing sentance number in brown_test out of first 10 sentances
lattic_emission = [[] for i in range(l)]  #emission probability lattic
sen_tag = []                              #set of all different tags sentance can have 
for i in range(l):
    for j in probWiti:
        if sentance[i][0] == j[0][0]: 
            lattic_emission[i].append(j) #lattice will only have element whose emission probability > 0, b/z for 0 emission probability final probability become zero
            if j[0][1] not in sen_tag:
                sen_tag.append(j[0][1]) #set of all posible taggs s sentance can have
    if(len(lattic_emission[i])== 0):    #for unknown words in sentance 
        temp = [(sentance[i][0], 'NN') , 0.11 ] # unk are consider as 'NN' with probability of 0.11 b/w 11% accuracy is for unknoen wors as ' 
        lattic_emission[i].append(temp)
                
       
            
#transition tags for this sentance
l = len(sen_tag) 
tran_tag = []
for i in sen_tag:
    for j in sen_tag:
        temp = (i , j)
        if temp not in tran_tag: # avoid repetitions 
            tran_tag.append(temp)
            

            
#transition probability for this sentance
tran_pro = []
for i in tran_tag:
    for j in probbitag:
        if i == j[0]:  
            tran_pro.append(j) # the tag pairs not in probbitag have zero probability again we are not considering them since result for such sentace will have 0 probability
mat = []
for i in lattic_emission:
    temp = [i[0][0][0], len(i)]
    mat.append(temp)       # number of possible tags outcomes for given word in a given sentance 

max_emission = []
sequence = []
for i in lattic_emission:
    def sortthird(i): 
        return i[1] 
    i.sort(key = sortthird ,reverse = True) # getting maximum emission probability after each step
    max_emission.append(i)
l = len(mat)
vi = []
for i in range(l-1):
    if i < l:
        temp =(max_emission[i][0][0][1],max_emission[i+1][0][0][1])
        vi.append(temp)
        sequence.append(max_emission[i][0][0])
temp = ('<\s>', '<\s>')
sequence.append(temp)
l = len(vi)
Vj = [] #argmax from probability multiplication of transition and emission probabilities 
m = 0
for i in range(l):
    for j in tran_pro:
        m += 1
        if vi[i] == j[0]:
            temp = max_emission[i][0][1]*j[1]
            Vj.append(temp)
            temp1= [max_emission[i][0][0],j[0]]
    temp1= [max_emission[i][0][0],j[0]]
    if(temp1 not in sequence):
        temp1= [max_emission[i][0][0],j[0]]
        
def viterbi(Vj) : 
    result = 1
    for x in Vj: 
         result = result * x  
    return result         
Viterbi = viterbi(Vj)
print(sequence , '\n' ,Viterbi)

# the accuracy 
l = len(sentance)
count = 0
for i in range(l):
    if sentance[i] == sequence[i]:
        count +=1
accuracy = (count / len(sentance))*100
print("accuracy of HMM tagger for given sentance is ")
print(accuracy)     # we are getting accuracy less because of prase types, different prase futher have different pos tags which are algorithm does not consider some time 


            


# In[ ]:




# In[ ]:




# In[ ]:



