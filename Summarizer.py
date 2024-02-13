!pip install bs4
!pip install html5lib
!pip install lxml
!pip install nltk


import nltk
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
nltk.download("stopwords")
import urllib.request
import bs4 as BeautifulSoup

def read_article(filename):
    file=open(filename, "r")
    filedata=file.readlines()
    article=filedata[0]. split (".")
    Sentences=[]
    for sentence in article:
        print (sentence)
        Sentences.append(sentence.replace("[^a-zA-Z]", " "). split (" "))
    Sentences.pop()
    return Sentences

  
def sentence_similarity(S1,S2, stopwords=None):
    if stopwords is None:
        stopwords=[]
    S1=[w.lower() for w in S1]
    S2=[w.lower() for w in S2]
    All_words= list(set(S1+S2))
    Vector1=[0]*len(All_words)
    Vector2=[0]*len(All_words)
    for w in S1:
        if w in stopwords:
            continue
        Vector1[All_words.index(w)]+=1
    for w in S2:
        if w in stopwords:
            continue
        Vector2[All_words.index(w)]+=1


    return 1-cosine_distance(Vector1, Vector2)


def build_similarity_matrix(sentences,stop_words):
    similarity_matrix=np.zeros((len(sentences),len(sentences)))
    for idx1 in range (len(sentences)):
        for idx2 in range (len(sentences)):
            if idx1==idx2:
                continue
            similarity_matrix[idx1][idx2]=sentence_similarity(sentences [idx1], sentences [idx2],stop_words)
    return similarity_matrix


def wr_pa_ur():
    Article=urllib.request.urlopen(input ("Please give a URL"))
    text=Article.read()
    text_parsed=BeautifulSoup.BeautifulSoup(text,"lxml")
    Paragraphs=text_parsed.find_all("p")
    text_content=''
    for p in Paragraphs:
        text_content+=p.text
    article=text_content.split(".")
    sentences=[]
    for sentence in article:
        print (sentence)
        sentences.append(sentence.replace("[^a-zA-Z]","").split(" "))
    sentences.pop()
    return sentences


def generate_summary():
    stop_words=stopwords.words("english")
    summarize_text=[]
    sentences=wr_pa_ur()
    sentence_similarity_matrix=build_similarity_matrix(sentences,stop_words)
    sentence_similarity_graph=nx.from_numpy_array(sentence_similarity_matrix)
    scores=nx.pagerank(sentence_similarity_graph)
    ranked_sentence=sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    print ("indices of top ranked_sentence order are",ranked_sentence)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    print ("summarized text:\n",". ".join(summarize_text))


generate_summary()
