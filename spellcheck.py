
# coding: utf-8

# In[56]:


import re
from collections import Counter
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.corpus import brown
tokenizer = RegexpTokenizer(r'\w+')
# wordsRead = tokenizer.tokenize(open('big.txt', "r").read().lower())
wordsRead = brown.words()

WORDS     = {w:0 for w in wordsRead}
#big.txt,along with other pointers for this project taken from peter norvig's blog...
WordCounts  =   Counter(wordsRead)
TotalWords  = len(WordCounts)
bgrams      = nltk.bigrams(wordsRead)
bgramsFreq  = dict(nltk.ConditionalFreqDist([((w),w2) for w,w2 in bgrams]))


# In[49]:


def findEdits(word):
        #do one change and two changes.
        edits   = set()
        letters = 'abcdefghijklmnopqrstuvwxyz'
        spliced = [(word[:i],word[i:]) for i in xrange(len(word))]
        for sp in spliced:
            #deletions
            sp0 = sp[0]
            sp1 = sp[1]
            deletion = sp0+sp1[1:]
            if deletion in WORDS:
                edits.add(deletion)
            #transposition
            if len(sp1)>1:
                transposition = sp0 + sp1[1] + sp1[0] + sp1[2:]
                if transposition in WORDS:
                    edits.add(transposition)
            for l in letters:
                #insertions
                insertion = sp0+l+sp1
                if insertion in WORDS:
                    edits.add(insertion)
                #substitutions
                substitute = sp0 + l +sp1[1:]
                if substitute in WORDS:
                    edits.add(substitute)
        return edits


# In[3]:


def findPossibleEdits(word):
     distance1 = findEdits(word)
     distance2 = set()
     for word in distance1:
         distance2 = distance2.union(findEdits(word))
     return distance1.union(distance2)


# In[11]:


def getBgramEdits(word,preword,postword,possibleEdits):
    editsProb = []
    t    = dict(bgramsFreq[preword]) if preword in bgramsFreq else {}
    for edit in possibleEdits:
        u    = dict(bgramsFreq[edit])
        te   = t[edit] if edit in t else 0
        up   = u[postword] if postword in u else 0
        teProb= (te+0.0005)/sum(t.values()) if t else 0
        upProb=(up+0.0005)/sum(u.values())  if u else 0
        prob = teProb + upProb
        editsProb.append((edit,prob))
    return editsProb


# In[39]:


def suggestEdit(word,preword,postword,possibleEdits):
    suggestions = []
    bgramEdits  = getBgramEdits(word,preword,postword,possibleEdits)
    t    = dict(bgramsFreq[preword]) if preword in bgramsFreq else {}
    u    = dict(bgramsFreq[word])
    te   = t[word] if word in t else 0
    up   = u[postword] if postword in u else 0
    teProb= (te+0.0005)/sum(t.values()) if t else 0
    upProb=(up+0.0005)/sum(u.values())  if u else 0
    currentBgram = teProb+ upProb
    for edit,prob in bgramEdits:
        if prob > (currentBgram*5.0):
            suggestions.append((edit,prob))
    return suggestions


# In[44]:


def check(string):
    s = string.split(' ')
    lens = len(s)
    edits = {}
    suggestionsD= {}
    for i in xrange(lens):
        word = s[i]
        if word.lower():
            word = re.match('\w+', word.lower()).group(0)
            preword=""
            postword=""
            if (i-1)>=0:
                preword = re.match('\w+', (s[i-1]).lower()).group(0)
            if (i+1)<lens:
                postword = re.match('\w+', (s[i+1]).lower())
                if postword:
                    postword = postword.group(0)
            if word not in WORDS:
                possibleEdits = findPossibleEdits(word)
                editRanks = []
                bgramEdits=[]
                #add in their probabilities...
                if i>0 and (i+1)<lens:
                    bgramEdits    = getBgramEdits(word,preword,postword,possibleEdits)
                for edit in possibleEdits:
                    editRanks.append((edit,WordCounts[edit]))
                if possibleEdits:
                    edits[word]={"unigram":sorted(editRanks, key=lambda tup:tup[1], reverse=True)[:3], "bigram":sorted(bgramEdits,key=lambda tup:tup[1], reverse=True)[:3]}
                else:
                    print "{} is not in the dictionary".format(word)
            else:
                #do the bigram checkeru for edits of correct words!
                suggestions = suggestEdit(word,preword,postword,findEdits(word))
                if suggestions:
                    suggestionsD[word] = {"suggestions":sorted(suggestions, key=lambda tup:tup[1],reverse=True)[:1]}
    return edits,suggestionsD
