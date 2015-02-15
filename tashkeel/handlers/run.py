from DBHandler import DBHandler
from MyToolKit import MyToolKit
import os,codecs,nltk
from pprint import pprint
from collections import defaultdict
import re

diac = [ 'َ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ', 'ّ', 'ُ']
def saveSents(corpuspath,diacratic):
    l = []
    tool = MyToolKit()
    hdb = DBHandler("model.db")
    for path, dirs, files in os.walk(corpuspath):
        for f in files:
            if f.startswith('_') != diacratic :
                print("Traiter le fichier : "+path+'/'+f)
                f = codecs.open(path+'/'+f,'r', encoding='utf-8').read()
                #f = f.replace('||', ' ')
                l += tool.sents(f,["\n","\r",".",":",",",';'],subsent=['"',"'",'-'])
    l2 = []
    for a in l:
        #Eliminé les phrases qui ont un seul mot (problème de nettoyage)
        if len(tool.words(a))>1 : l2.append("# "+a+" $")
    print("Création de la distribution de fréquences ...")
    fdist = nltk.FreqDist(l2)
    print("OK !")
    print("Convertir la liste en cours ...")
    data = []
    for fd in fdist: data.append([fd,fdist[fd]])
    print("Stocker les phrases base de données !")
    hdb.connect()
    if diacratic == True : hdb.insertIntoTable('sents_all',data)
    else : hdb.insertIntoTable('sents',data)
    print("OK !")

def DeleteDiacritic(txt):
    teshkeel = [ 'َ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ', 'ّ', 'ُ']
    for shakl in teshkeel: txt = txt.replace(shakl , "")
    return txt
def normalizeArabicAlif(text) :
    text = re.sub('[إأٱآا]','ا',text)
    return text

def have_diac(word):
    for char in list(word):
        if char in diac: return True
    return False

def saveWord():
    tool = MyToolKit()
    hdb = DBHandler("model.db")
    print("Récuperation des phrases (with diacratic) ...")
    hdb.connect()
    sents = hdb.getFromTable('sents_train')
    print("Done !")
    print("Récuperations des mots, et Création des distributions de fréquences ...")
    words = []
    fdist = nltk.FreqDist()
    #words = []
    for sent in sents:
        for word in tool.words(sent[1]):
            #word_without_diac = tool.DeleteDiacritic(word)
            #if len(word) > 1 or word == 'و':
            if have_diac(word)==True or word == '#' or word == '$' : fdist[word] = fdist[word]+sent[2]


    print("Done !")

    print("Convertion des listes en cours ...")
    data = []
    #data = []
    #for fd in fdist: data.append([fd,fdist[fd]])
    for fd in fdist: data.append([fd,fdist[fd]])
    print("OK !")
    print("Stocker les mots dans la base de données :")
    print("With diac ...")
    hdb.insertIntoTable('words',data)
    print("Done !")

def saveNormalizedWord():
    tool = MyToolKit()
    hdb = DBHandler("model.db")
    print("Récuperation des phrases (with diacratic) ...")
    hdb.connect()
    sents = hdb.getFromTable('sents_train')
    print("Done !")
    print("Récuperations des mots, et Création des distributions de fréquences ...")
    words = []
    fdist = nltk.FreqDist()
    #words = []
    for sent in sents:
        for word in tool.words(sent[1]):
            #word_without_diac = tool.DeleteDiacritic(word)
            #if len(word) > 1 or word == 'و':
            if have_diac(word)==True or word == '#' or word == '$' : fdist[normalizeArabicAlif(word)] = fdist[normalizeArabicAlif(word)]+sent[2]

    print("Done !")

    print("Convertion des listes en cours ...")
    data = []
    #data = []
    #for fd in fdist: data.append([fd,fdist[fd]])
    for fd in fdist: data.append([fd,fdist[fd]])
    print("OK !")
    print("Stocker les mots dans la base de données :")
    print("With diac ...")
    hdb.insertIntoTable('words_normalized',data)
    print("Done !")

def saveNgramsDiac(n):
    tool = MyToolKit()
    hdb = DBHandler("model.db")
    print(":::: Statistique Ngrams("+str(n)+") ::::")
    print("Récuperation des phrases (with diacratic) ...")
    hdb.connect()
    sents = hdb.getFromTable('sents_train',attribute='sent')
    print("Done !")
    print("Création des Ngrams ...")
    grams = []
    for sent in sents: grams += nltk.ngrams(tool.words(sent[0]),n)

    print("Done !")
    print("Création de la distribution de fréquences ...")
    fdist = nltk.FreqDist(grams)
    print("Done !")

    print("Convertion des listes en cours ...")
    data = []
    for fd in fdist: data.append([' '.join(fd),fdist[fd]])
    print("OK !")

    print("Stocker les mots dans la base de données :")
    hdb.insertIntoTable('grams'+str(n),data)
    print("Done !")

def creatDict():
    tool = MyToolKit()
    hdb = DBHandler("model.db")
    print("Récuperation des mots (with diacratic) ...")
    hdb.connect()
    words = hdb.getFromTable('words')
    print("Done !")

    print("Création du dictionnaire ...")
    dict = defaultdict(list)
    for tuple in words:
        dict[DeleteDiacritic(normalizeArabicAlif(tuple[1]))].append(tuple[1])
    data = []
    print("Done !")

    print("Convertion de la liste en cours ...")
    for type in dict:
        data.append((type,' '.join(dict[type])))
    print("Done !")
    print("Stocker le dictionnaire dans la base de données :")
    hdb.insertIntoTable('dictionary',data)
    print("Done !")
#Save sents (whith and without diacratics)
saveSents('corpus',False)
#saveSents('corpus',True)

#Save words (whith and without diacratics)
saveWord()
#saveNormalizedWord()
#Save Ngrams (whith and without diacratics)
saveNgramsDiac(2)
#saveNgramsDiac(3)
#saveNgramsDiac(4)
creatDict()
