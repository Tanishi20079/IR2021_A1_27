# -*- coding: utf-8 -*-
"""IR2021_A1_27

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sDnL4L-qBp4rfMT1E_iDqEryfF3cwAH4
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import re
import numpy as np
import pandas as pd
import nltk
import nltk
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

#nltk.download('stopwords')

# Getting path of folder stories and folders inside it

getPath = str('/content/drive/MyDrive/stories')
print(getPath)
getAllFolders = [x[0] for x in os.walk(getPath)]

getAllFolders.pop(len(getAllFolders)-1)
print(getAllFolders)

#After analysing we found index.html that contains all the file names and titles
# create a tuple of all files path and title

list_of_all_files = []
flag = 0
for i in getAllFolders:
    path = i+"/index.html"
    print(path)
    openIndexFile = open(path, 'r')
    getContent = openIndexFile.read().strip()
    openIndexFile.close()
    
    # file name is enclosed in Anchor tag of html file
    getFileName = re.findall('><A HREF="(.*)">', getContent)
    #print(getFileName)
    
    # file title is enclosed in <BR><TD> tag of html file
    getFileTitle = re.findall('<BR><TD> (.*)\n', getContent)
    #print(len(getFileTitle))
    
    #for excluding folder inside stories which are at 0th and 1st index
    if flag==0:
        getFileName = getFileName[2:]
        flag = 1
    for j in range(len(getFileName)):
        list_of_all_files.append((str(i)+"/" + str(getFileName[j]), getFileTitle[j]))
    
#print(len(list_of_all_files))

#Convert data in to lower case
def lower(text):
    return np.char.lower(text)

# remove all the stopwords(‘off’, ‘is’, ‘s’, ‘am’, ‘or’, ‘who’, e.t.c) from data
def stopWords(text):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(text))
    new_text = ""
    for w in words:
        if w not in stop_words:
            new_text = new_text + " " + w
    return np.char.strip(new_text)

# remove all the punctuation symbols
def punctuationSymbols(text):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        text = np.char.replace(text, symbols[i], ' ')
        text = np.char.replace(text, "  ", " ")
        text = np.char.replace(text, ',', '')
    return text

# remove all apostrophes  
def unUsed(text):
    return np.char.replace(text, "'", "")

# remove all the one length words
def lengthOneChar(text):
    words = word_tokenize(str(text))
    new_text = ""
    for j in words:
        if len(j) > 1:
            new_text = new_text + " " + j
    return np.char.strip(new_text)

# replace numeric values to their coreesponding text value
def deleteNumerics(text):
    text = np.char.replace(text, "0", " zero ")
    text = np.char.replace(text, "1", " one ")
    text = np.char.replace(text, "2", " two ")
    text = np.char.replace(text, "3", " three ")
    text = np.char.replace(text, "4", " four ")
    text = np.char.replace(text, "5", " five ")
    text = np.char.replace(text, "6", " six ")
    text = np.char.replace(text, "7", " seven ")
    text = np.char.replace(text, "8", " eight ")
    text = np.char.replace(text, "9", " nine ")
    return text

#perform stemming
def performStemming(text):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(text))
    new_text = ""
    for j in tokens:
        new_text = new_text + " " + stemmer.stem(j)
    return np.char.strip(new_text)

#call all the above functions to preprocess the data
def preprocess(data, query):    
    data = lower(data)
    data = stopWords(data)
    data = punctuationSymbols(data) #remove comma seperately
    data = unUsed(data)
    data = deleteNumerics(data)
    data = lengthOneChar(data)
    data = performStemming(data)
    # data = lemma(data)
    return data

num = 0
listsOfDocs = pd.DataFrame()
for i in list_of_all_files:
    #for reading files with all the extensions including .txt
  with open(i[0], 'r', encoding = 'utf-8', errors = 'ignore') as f2:
    text = f2.read().strip()
    f2.close()
    #call preprocess for each file 
    preprocessed_text = preprocess(text, False)
    js = word_tokenize(str(preprocessed_text))

    #making posting lists for words
    for j in js:
      if j in listsOfDocs:
        p = listsOfDocs[j][0]
        p.add(num)
        listsOfDocs[j][0] = p
      else:
        listsOfDocs.insert(value=[{num}], loc=0, column=j)
    num += 1



#converting dataframe postings to dictionary
df = {}
for i in listsOfDocs:
  df[i] = listsOfDocs[i][0]

#df['thought']

#Creating set for all documents
totals = set()
for i in range(467):
  totals.add(i)

# this will pick up two words and corresponding operator respectively
def evaluateQuery(data,query):
  com = 0
  print(data)
  print(query)
  while len(data)>1:
    first = data.pop(0)
    second = data.pop(0)
    operator = query.pop(0)
    print(first,operator,second)
    # if OR operator calling applyOr function
    if (operator == 'OR'):
      x,y = applyOr(first,second)
      com += x
      data.insert(0,'calculated')
      df['calculated'] = y
    # if AND operator calling applyAnd function
    elif (operator == 'AND'):
      x,y = applyAnd(first,second)
      com += x
      data.insert(0,'calculated')
      df['calculated'] = y
    # if AND operator calling applyNotAnd function
    elif (operator == 'AND NOT'):
      x,y = applyNotAnd(first,second)
      com += x
      data.insert(0,'calculated')
      df['calculated'] = y
    # if OR operator calling applyNotOr function
    elif (operator == 'OR NOT'):
      x,y = applyNotOr(first,second)
      com += x
      data.insert(0,'calculated')
      df['calculated'] = y

  #Printing result
  print('Number of documents matched: ',len(df['calculated']))
  print('No. of comparisons required: ',com)


#calculate Or (union)
def applyOr(first,second):
  Or = []
  firstPosting = list(df[first])
  secondPosting = list(df[second])
  i=0
  j=0
  comparison = 0
  while i<len(firstPosting) or j<len(secondPosting):
    if i<len(firstPosting) and j<len(secondPosting) and (firstPosting[i]==secondPosting[j]):
      comparison+=1
      Or.append(firstPosting[i])
      i+=1
      j+=1
    elif i < len(firstPosting)and j<len(secondPosting) and (firstPosting[i]<secondPosting[j]):
      comparison+=1
      Or.append(firstPosting[i])
      i+=1
    elif i < len(firstPosting)and j<len(secondPosting) and (firstPosting[i]>secondPosting[j]):
      comparison+=1
      Or.append(secondPosting[j])
      j+=1
    elif i < len(firstPosting):
      Or.append(firstPosting[i])
      i+=1
    elif j<len(secondPosting):
      Or.append(secondPosting[j])
      j+=1

  return comparison,set(Or)

#Calculate And(Intersection)
def applyAnd(first,second):
  And = []
  firstPosting = list(df[first])
  secondPosting = list(df[second])
  i=0
  j=0
  comparison = 0
  while i<len(firstPosting) and j<len(secondPosting):
    if (firstPosting[i]==secondPosting[j]):
      And.append(firstPosting[i])
      i+=1
      j+=1
    elif (firstPosting[i]<secondPosting[j]):
      i+=1
    else:
      j+=1
    comparison+=1
  return comparison,set(And)

#Calculate Not
def notOperation(ls):
  temp = set()
  for i in totals:
    if i not in ls:
      temp.add(i)
  return temp

#Calculate Not Or
def applyNotOr(first,second):
  Or = []
  firstPosting = list(df[first])
  secondPosting = df[second]
  secondPosting = list(notOperation(secondPosting))
  i=0
  j=0
  comparison = 0
  while i<len(firstPosting) or j<len(secondPosting):
    if i<len(firstPosting) and j<len(secondPosting) and (firstPosting[i]==secondPosting[j]):
      comparison+=1
      Or.append(firstPosting[i])
      i+=1
      j+=1
    elif i < len(firstPosting)and j<len(secondPosting) and (firstPosting[i]<secondPosting[j]):
      comparison+=1
      Or.append(firstPosting[i])
      i+=1
    elif i < len(firstPosting)and j<len(secondPosting) and (firstPosting[i]>secondPosting[j]):
      comparison+=1
      Or.append(secondPosting[j])
      j+=1
    elif i < len(firstPosting):
      Or.append(firstPosting[i])
      i+=1
    elif j<len(secondPosting):
      Or.append(secondPosting[j])
      j+=1

  return comparison,set(Or)


#Calculate Not And
def applyNotAnd(first,second):
  And = []
  firstPosting = list(df[first])
  secondPosting = df[second]
  secondPosting = list(notOperation(secondPosting))
  i=0
  j=0
  comparison = 0
  while i<len(firstPosting) and j<len(secondPosting):
    if (firstPosting[i]==secondPosting[j]):
      And.append(firstPosting[i])
      i+=1
      j+=1
    elif (firstPosting[i]<secondPosting[j]):
      i+=1
    else:
      j+=1
    comparison+=1
  return comparison,set(And)

#Check if query asked is valid to our documents
def check_data(data):
  for i in data:
    if i not in df:
      return 0

#taking input and preprocessing it
inp = input("Enter input : ")
data = preprocess(inp,False)
data = data.item(0).split()
if (check_data(data)==0):
  print('Invalid Query')
else:
  #print(type(data))
  #print(len(data))
  query = input("Query : ") 
  query = query.split(',')
  queryList = []
  for i in range(len(query)):
    p = query.pop()
    p = p.replace('[',"")
    p = p.replace(']',"")
    p = p.strip()
    queryList.append(p)
  evaluateQuery(data,queryList)

# if takeInput()==1: 
#   evaluateQuery(data,queryList)
# else:
#   print('Invalid Query')

