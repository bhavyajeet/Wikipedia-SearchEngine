import sys
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from tqdm import tqdm_notebook as tqdm
import math
import xml.sax
import bisect
from collections import defaultdict


from nltk.corpus import stopwords 
from Stemmer import Stemmer

stop_words = set(stopwords.words('english')) 
stemmer = Stemmer('porter')


stemmer = Stemmer('porter')

#inpstr = input("enter qry: ")

filer = open('./complete/secondary.txt', 'r')
secwords = filer.readlines()
filer.close()

def getpost(tok):
    position = bisect.bisect(secwords,tok+'\n') -1 
    #print (str(position) + " is the position")
    if position < 0 :
        return -1
    else :
        corfile = open('./complete/fin' + str(position) + '.txt', 'r')
        line = corfile.readline().strip('\n')
        while line:
            spltwrd = line.split(":")
            if spltwrd[0] == tok:
                return spltwrd[1]
            line = corfile.readline().strip('\n')
        return -1

def gettitle(doc_no):
    titlethreshold = 1500
    off = doc_no // titlethreshold
    file = open("./fintitle/title" + str(off+1) + '.txt')
    return file.readlines()[doc_no % titlethreshold].strip('\n')


def tokenize(text):
    text=text.lower()
    tokens = re.split(r'[^A-Za-z0-9]+', text)
    final = []
    for token in tokens:
        # print(token,' is token')
        word = stemmer.stemWord(token)
        # word = token
        if len(word) <= 1 or word in stop_words :
            continue
        final.append(word)
    # print (final)
    return final

fieldtype = ['t', 'b', 'r', 'c', 'l', 'i']
fieldmap = {'t':0, 'b':1, 'r':2, 'c':3, 'l':4, 'i':5}

def getnum(docpost):
    toret = ['','','','','','']
    curr='d'
    flag=  0
    for i in docpost:
        if i in fieldtype:
            curr=i
            flag+=1
        elif (i not in fieldtype) and flag  :
            toret[fieldmap[curr]]+=i
    for i in range(len(toret)):
        if toret[i] == '':
            toret[i]=0
        else :
            toret[i] = int(toret[i])
    #print (toret)
    return toret
        


doccount = 9800000
strtoprint=[]
intlist = ['0','1','2','3','4','5','6','7','8','9']
def dosearch(inpstr):
    global strtoprint
    scorer = defaultdict(lambda : [0] * 8)
    scorer = defaultdict(int)
    if inpstr.find(':') == -1:
        k=int(inpstr.split(',')[0])
        inpstr=inpstr.split(',')[1]
        lis = tokenize(inpstr)
        #print(lis)
        for tok in lis :
            postlist = getpost(tok)
            if postlist != -1 :
                tokcount = defaultdict(int)
                doclist = postlist.split("d")[1:]
                dn = len(doclist)
                idf = math.log2(doccount/dn)
                #print ("idf for ",tok," is ", str(idf))
                for  docy in doclist:
                    pageid=''
                    for i in docy:
                        if i not in intlist:
                            break
                        else :
                            pageid+=i
                    pageid=int(pageid) 
                    #print(str(pageid))
                    scores = getnum(docy)
                    scores[0]*=200
                    scores[1]*=5*2
                    scores[2]*=4*2
                    scores[3]*=4*2
                    scores[4]*=4*2
                    scores[5]*=28
                    for i in scores:
                        tokcount[pageid]+=i
                    scorer[pageid]+=math.log2(tokcount[pageid])*idf
                #print (sorted(scorer.items(), key=lambda x: x[1], reverse = True))
        final = sorted(scorer.items(), key=lambda x: x[1], reverse = True)
        lenfin=len(final)
        for i in range (0,min(k,lenfin)):
            strtoprint.append(str(final[i][0]) + ',' + gettitle(final[i][0]) + '\n')
            #print ("id:",final[i][0]," title: ",gettitle(final[i][0]))
        if k > lenfin:
            for jl in range (k-lenfin):
                randpage = random.randint(0,9829058)
                strtoprint.append(str(randpage) + ',' + gettitle(randpage) + '\n')
    else :
        parsed = defaultdict(int)
        k=int(inpstr.split(',')[0])
        inpstr=inpstr.split(',')[1]
        prsd =[]
        lis = inpstr.split(":")
        first = False
        for kr in range(len(lis)):
            if not first:
                first =True 
            else :
                spltlst = lis[kr-1].split()
                contlst = lis[kr].split()
                category = spltlst[len(spltlst)-1]
                content = tokenize(' '.join(contlst))
                prsd.append((category,content))
        for i in range (len(prsd)):
            for tok in prsd[i][1]:
                parsed[tok]=prsd[i][0]
        #print (parsed)
        for tok in parsed.keys():
            postlist = getpost(tok)
            if postlist != -1 :
                tokcount = defaultdict(int)
                doclist = postlist.split("d")[1:]
                dn = len(doclist)
                idf = math.log2(doccount/dn)
                #print ("idf for ",tok," is ", str(idf))
                for  docy in doclist:
                    pageid=''
                    for i in docy:
                        if i not in intlist:
                            break
                        else :
                            pageid+=i
                    pageid=int(pageid) 
                    #print(str(pageid))
                    scores = getnum(docy)
                    scores[0]*=200
                    scores[1]*=5*2
                    scores[2]*=4*2
                    scores[3]*=4*2
                    scores[4]*=4*2
                    scores[5]*=28
                    scores[fieldmap[parsed[tok]]]*=10000
                    for i in scores:
                        tokcount[pageid]+=i
                    #print (scores)
                    scorer[pageid]+=math.log2(tokcount[pageid])*idf
                #print (sorted(scorer.items(), key=lambda x: x[1], reverse = True))
        final = sorted(scorer.items(), key=lambda x: x[1], reverse = True)
        lenfin = len(final)
        for i in range (0,min(k,lenfin)):
            strtoprint.append(str(final[i][0]) + ',' + gettitle(final[i][0]) + '\n')
            #print ("id:",final[i][0]," title: ",gettitle(final[i][0]))
        if k > lenfin:
            for jl in range (k-lenfin):
                randpage = random.randint(0,9829058)
                strtoprint.append(str(randpage) + ',' + gettitle(randpage) + '\n')
                

import random
qfname = sys.argv[1]
qfile = open (qfname,'r')
#line = qfile.readline()
lines = qfile.readlines()
#print(lines)
qfile.close()
import time
for liner in lines:
    st = time.time()
    dosearch(liner)
    en = time.time()
    ky=int(liner.split(',')[0])
    strtoprint.append(str(en-st)+","+ str((en-st)/ky) +'\n\n')

    
opfile = open ('queries_op.txt','a')
opfile.writelines(strtoprint)
opfile.close()

#while line :
#    dosearch(line)
#    line = qfile.readline()
