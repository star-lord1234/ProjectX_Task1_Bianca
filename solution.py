import spacy
import nltk

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('punkt') 
nltk.download('words')
lemmatizer = WordNetLemmatizer()

NER = spacy.load("en_core_web_lg")
test= input("Enter your statement: ")
tokens=word_tokenize(test)
poslist=pos_tag(tokens)

properN=[]
text1=NER(test)
for word in text1.ents:
     if word.label_!="DATE" and word.label_!="PRODUCT":
        if not any(char.isdigit() for char in word.text):
            properN.append(word.text)



wordset=set(words.words())
new_tokens=[]
corrections=[('1','l'),('5','s'),('0','o'),('h','b'),('e','c'),('b','h'),('c','e')]
for token, pos in poslist:
    if token in wordset or pos in ["NNP","NNPS"]:
        new_tokens.append(token)
        continue
    ns=token
    for y,z in corrections:
        if y in ns:
           trial= ns.replace(y,z,1)
           l=len(trial)
           if trial[l-1]=='s':
               tr=trial[:l-1]
           elif "ing" in trial:
               tr=lemmatizer.lemmatize(trial, 'v')
           else:
               tr=trial
           if tr in wordset:
               ns=trial
               
               break
    new_tokens.append(ns)


final_tokens = []

discourse_markers=['however', 'although', 'but', 'while']
i=0
for i in range(len(new_tokens)):
    token = new_tokens[i]
    final_tokens.append(token)
    if token.lower() in discourse_markers:
        if i + 1<len(new_tokens) and new_tokens[i + 1]!=',':
            final_tokens.append(',')
new=""
for t in final_tokens:
    new=new+t+" "
print(new)
print(properN)