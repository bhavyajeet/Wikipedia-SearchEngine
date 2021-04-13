import sys
from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
import re
from os import mkdir
from os import rename
import xml.sax
from collections import defaultdict
from nltk.corpus import stopwords 
from Stemmer import Stemmer

stop_words = set(stopwords.words('english')) 
stemmer = Stemmer('porter')

try:
    mkdir("inddir")
except:
    pass

indict=defaultdict(dict)

def indexer(title,body,references,categories,links,infobox,pagenum):
    global indict
    # indict[i][pagenum]=[0,0,0,0,0,0]
    for i in title:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]
        
        indict[i][pagenum][0]+=1
 
    for i in body:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]
 
        indict[i][pagenum][1]+=1

    for i in references:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]

        indict[i][pagenum][2]+=1

    for i in categories:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]

        indict[i][pagenum][3]+=1

    for i in links:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]

        indict[i][pagenum][4]+=1

    for i in infobox:
        try:
            indict[i][pagenum]
        except:
            indict[i][pagenum]=[0,0,0,0,0,0]

        indict[i][pagenum][5]+=1

   
    # print(indict)


indcount = 0 
totcount = 0 



def tokenize(text):
    global totcount
    tokens = re.split(r'[^A-Za-z0-9]+', text)
    final = []
    for token in tokens:
        totcount+=1
        word = stemmer.stemWord(token)
        # word = token
        if len(word) <= 1 or word in stop_words or len(word)>50:
            continue
        final.append(word)
    # print (final)
    return final


def getLinks(text):
    # print(text)
    ans = []
    raw = text.split("\n")
    for lines in raw:
        # print(lines)
        if lines and lines[0] == '*':
            # print("lololol link found")
            line = tokenize(lines)
            ans += line
    # print (ans)
    return ans 


brcount =0 
uncount =0 
def getInfobox(text):
    global uncount
    global brcount 
    cont = text.split("{{infobox")
    info = []
    if len(cont) <= 1:
        uncount += 1 
        return []
    # if len(cont)>2:
    #     brcount+=1
    flag= False
    for infob in cont:
        traw = infob.split("\n")
        if (not flag):
            flag=True
        else :
            for lines in traw:
                # print (lines)
                if lines == "}}":
                    break
                info += tokenize(lines)
    # print (info)
    return info


def getReferences(text):
    refarr = []
    reflist = re.findall(r'\|\s*title[^\|]*',text)
    for i in reflist:
        refarr.append(i.replace('title','',1))
    # print("++++")
    # print(reflist)
    return (tokenize(' '.join(refarr)))



def getCategories(text):
    categoryList = re.findall(r"\[\[category:(.*)\]\]",text)
    return (tokenize(' '.join(categoryList)))



def processContent(text):
    text=text.lower()
    references=[]
    links=[]
    categories=[]
    data=text.split('==references==')
    if data[0] == text:
        data= text.split('== references ==')
    if data[0]==text:
        data= text.split('== references==')
    if data[0]==text:
        data= text.split('==references ==')
    if len(data)==1:

        categories = getCategories(data[0])

        haslink=1
        catdata=data[0].split('==external links==')
        if len(catdata)==1:
            catdata=data[0].split('==external links ==')	
        if len(catdata)==1:
            catdata=data[0].split('== external links==')
        if len(catdata)==1:
            catdata=data[0].split('== external links ==')
        if len(catdata)==1:
            links=[]
            haslink=0
        if (haslink):
            links=getLinks(catdata[1])



    else:

        haslink=1
        catdata=data[1].split('==external links==')
        if len(catdata)==1:
            catdata=data[1].split('==external links ==')	
        if len(catdata)==1:
            catdata=data[1].split('== external links==')
        if len(catdata)==1:
            catdata=data[1].split('== external links ==')
        if len(catdata)==1:
            links=[]
            haslink=0
        if (haslink):
            links = getLinks(catdata[1])
        
        references = getReferences(data[1])
        categories = getCategories(data[1])
        # links = getlinks(data[1])
    infobox= getInfobox(data[0])
    body = tokenize(data[0])
    return body, references, categories, links, infobox
    

def printDisk():
    global indict
    global titlearr
    global tempfilecount

    f=open('title'+str(tempfilecount)+'.txt','w')
    f.writelines(titlearr)
    f.close()
    titlearr=[]

    # cntr = cntr - 1
    fieldtype = ['t', 'b', 'r', 'c', 'l', 'i']
    namer = "inddir/"+ 'index' + str(tempfilecount) + '.txt'
    file = open(namer, 'w')
    ind=0
    for word in (sorted(indict.keys())):
        mystr = word + ':'
        for doc in indict[word]:
            posting = indict[word][doc]
            mystr += "d" + str(doc)
            ct=0
            for  fs in (posting):
                if fs > 0:
                    mystr += str(fieldtype[ct]) + str(fs)
                ct+=1
        file.write(mystr + "\n")
        ind+=1
    indict=defaultdict(dict)
    tempfilecount+=1
    print ("created file "+str(tempfilecount-1))
    file.close()
    # print(cntr)
    # file = open("./titles/title" + str(cntr) + ".txt", 'w')
    # for title in titles:
    #     file.write(title + '\n')
    # file.close()





def mergefiles(a,b):
    print ("merging files "+ str(a)+" and "+str(b))
    file1 = open('inddir/index'+str(a)+'.txt','r')
    file2 = open('inddir/index'+str(b)+'.txt','r')
    newfile = open('inddir/'+"strb"+'.txt','w')
    line1 = file1.readline()
    line2 = file2.readline()
    while (line1 and line2 ):
        linespl1 = line1.split(':')
        linespl2 = line2.split(':')
        if linespl1[0] < linespl2[0]:
            newfile.write(line1)
            line1 = file1.readline()
        elif linespl2[0] < linespl1[0] : 
            newfile.write(line2)
            line2 = file2.readline()
        elif linespl1[0] == linespl2[0] :
            newfile.write(linespl1[0]+':' + linespl1[1].strip() + linespl2[1]) 
            line1 = file1.readline()
            line2 = file2.readline() 
    while (line1):
        newfile.write(line1)
        line1 = file1.readline()
    while (line2):
        newfile.write(line2)
        line2 = file2.readline()
    file1.close()
    file2.close()
    newfile.close()












def processTitle(title):
    return tokenize(title.lower())

class PageHandler(xml.sax.ContentHandler):

    global pageCount
    def __init__(self):
        print("called once")
        self.CurrentData = ''
        self.title = ''
        self.text = ''
        self.data = ''

    def startElement(self, tag, attributes):
        self.CurrentData = tag


    def endElement(self, tag):
        global titlearr
        if tag == 'page':
            global pageCount
            self.title = self.title.strip()
            titlearr.append(self.title+'\n')
            title = processTitle(self.title)
            body,references,categories,links,infobox = processContent(self.text)

            self.text=''
            self.title=''
            indexer(title,body,references,categories,links,infobox,pageCount)
            pageCount += 1
            # print ("printing at: file-"+ str(tempfilecount)+ " page-"+str(pageCount))
            if pageCount == tempfilecount * docthreshold:
                print(pageCount)        
                printDisk()
            # print('page ra')

    def characters(self, content):
        if self.CurrentData == 'title':
            self.title += content
        elif self.CurrentData == 'text':
            self.text+=content
        # elif tag == 'text':
        #     print (self.CurrentData)






def merge():
    mergefiles(1,2)
    rename('inddir/strb.txt','inddir/index0.txt')
    for i in range (3,tempfilecount):
        mergefiles(0,i)
        rename('inddir/strb.txt','inddir/index0.txt')



        
import os

global pageCount
titlearr = []
tempfilecount = 1 
docthreshold = 1500
tokthreshold = 15000
pageCount = 0
# f1 = sys.argv[1]
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler(Handler)
directory = './phase2-unzip'

for filename in os.listdir(directory):
    print(filename)
    parser.parse('./phase2-unzip/'+filename)
# print (brcount)
# print (uncount)
printDisk()
# merge()
