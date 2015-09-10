__author__ = 'bukun'

import pickle

class cNode(object):
    def __init__(self):
        self.children = None

# The encode of word is UTF-8
# The encode of message is UTF-8

class cDfa(object):
    def __init__(self):
        # self.pklfile = 'sdaf.pkl'
        self.root=cNode()

    # The encode of word is UTF-8
    def addWord(self,word):
        node = self.root
        iEnd=len(word)-1
        for i in range(len(word)):
            if node.children == None:
                node.children = {}
                if i!=iEnd:
                    node.children[word[i]]=(cNode(),False)
                else:
                    node.children[word[i]]=(cNode(),True)

            elif word[i] not in node.children:
                if i!=iEnd:
                    node.children[word[i]]=(cNode(),False)
                else:
                    node.children[word[i]]=(cNode(),True)
            else: #word[i] in node.children:
                if i==iEnd:
                    Next,bWord=node.children[word[i]]
                    node.children[word[i]]=(Next,True)

            node=node.children[word[i]][0]

    def isContain(self,sMsg):
        root=self.root
        iLen=len(sMsg)
        for i in range(iLen):
            p = root
            j = i
            while (j<iLen and p.children!=None and sMsg[j] in p.children):
                (p,bWord) = p.children[sMsg[j]]
                if bWord:
                    # markit()
                    # containwhich(sMsg)
                    # markit()
                    return True
                j = j + 1
        return False
    def filter(self,sMsg):
        lNew=[]
        root=self.root
        iLen=len(sMsg)
        i=0
        bContinue=False
        while i<iLen:
            p=root
            j=i
            while (j<iLen and p.children!=None and sMsg[j] in p.children):
                (p,bWord) = p.children[sMsg[j]]
                if bWord:
                    #print sMsg[i:j+1]
                    lNew.append(u'*'*(j-i+1))#关键字替换
                    i=j+1
                    bContinue=True
                    break
                j=j+1
            if bContinue:
                bContinue=False
                continue
            lNew.append(sMsg[i])
            i=i+1
        return ''.join(lNew)

filter = cDfa()
kwf = './resource/keywords.pkl'
with open(kwf,'rb') as fi:
    # print(fi)
    keywords_set = pickle.load(fi)
for keyword in keywords_set:
    filter.addWord(keyword)
# normal()
del(keywords_set)

def containwhich(msg_str):
    tmp_fi = open(kwf,'rb')
    tmp_keywords_set = pickle.load(tmp_fi)
    for x in tmp_keywords_set:
        # print('a' + x)
        if x in msg_str:
            # print(x)
            return

