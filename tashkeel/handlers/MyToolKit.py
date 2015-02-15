__author__ = 'Youcef'
import nltk,re
from pprint import pprint
from nltk.tokenize.regexp import RegexpTokenizer
class MyToolKit:
    diac = ['َ','ِ','ً','ٌ','ٍ','ْ','ّ','ُ']

    #noisy_diac=['\sَ\s','\sِ\s','\sً\s','\sٌ\s','\sٍ\s','\sْ\s','\sّ\s','\sُ\s']
    """
    separator : un tableau qui contient les séparateurs qui sépare les phrases (l'ordre est important)
    subsent : un tableau qui contient les caractéres qui limitent les sous chaine.
              par exemple le " (la chaine "pour comprendre la récurcivité, il faut comprendre la récursivité" est un exemple)
 |
    """
    def sents(self,text,separator,subsent=None):
        #pprint(text)
        sents = [text]

        for sep in separator:
            temp = []
            for el in sents:
                if el.strip() != "" and len(el)>1:
                    temp += el.strip().split(sep)
            sents = temp
        if subsent:
            for cont in subsent:
                temp = []
                for sent in sents:
                    list = re.findall("\s"+cont+'([\d|\w|\s|\.|,|?|!|'+'|'.join(self.diac)+']+)'+cont+"\s",sent)
                    for s in list:
                        s = re.sub("[a-z|A-Z|\d|\{|\}|\(|\)|\-|\*|%|\[|\]|\?|\؟|\!|\"|\'|/]", "", s)
                        for d in self.diac: s = s.replace(" "+d+" "," ")
                        if s.strip() != "" and len(s)>1: temp.append(s.strip())
                    for s in list: sent = re.sub("  "," ",re.sub(cont+s+cont, "", sent))
                    sent = re.sub("[a-z|A-Z|\d|\{|\}|\(|\)|\-|\*|%|\[|\]|\?|\؟|\!|\"|\'|/]", "", sent)
                    for d in self.diac: sent = sent.replace(" "+d+" "," ")
                    if sent.strip() != "" and len(sent)>1: temp.append(sent.strip())
                sents = temp
        return sents

    def words(self,text):
        reg_words = r'[\#|\$|\w|َ|ِ|ً|ٌ|ٍ|ْ|ّ|ُ]+'
        tokenizer = RegexpTokenizer(reg_words, flags=re.UNICODE|re.IGNORECASE)
        return tokenizer.tokenize(text)


    def CountWords(self,text):
        tool = MyToolKit()
        sents = tool.sents(text,["\n","\r",".",":",",",';'],subsent=['"',"'",'-'])
        nbr_words = 0
        for sent in sents: nbr_words += len(tool.words(sent))
        return nbr_words

    def CountCorrectVocalisedWords(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        nbr_words = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                if words1[j] == words2[j]: nbr_words += 1
        return nbr_words

    def HasDiac(self,word):
        for char in word:
            if char in self.diac: return True
        return False

    def LettersDiac(self,string):
        letters = []
        z = ""
        for char in string:
            if char not in self.diac :
                if z : letters.append(z)
                z = char
            else : z += char
        letters.append(z)
        return letters
    
    def HideChar(self,word,expect = None):
        if expect == None : expect = []
        for char in list(word):
            if char not in self.diac and char not in expect: 
                word = word.replace(char , "_")
        return word
    

    def DeleteDiacritic(self,txt):
        teshkeel = [ 'َ', 'ِ', 'ً', 'ٌ', 'ٍ', 'ْ', 'ّ', 'ُ']
        for shakl in teshkeel: txt = txt.replace(shakl , "")
        return txt

    def normalizeArabicAlif(self,text) :
        text = re.sub('[إأٱآا]','ا',text)
        return text
    
    
    
    
    
    
    
    
    
##################################################################
    def wer1_Recall(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        cp_sim_words = 0
        cp_words = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                if self.HasDiac(words2[j]) and words1[j] == words2[j]: cp_sim_words += 1
                cp_words += 1
        if cp_words == 0 : return 0
        return 100-(100*cp_sim_words/cp_words)

    def wer1_Precision(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        cp_sim_words = 0
        cp_diac = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                if self.HasDiac(words2[j]) and words1[j] == words2[j]:  cp_sim_words += 1
                if self.HasDiac(words2[j]) : cp_diac += 1
        if cp_diac == 0 : return 0
        return 100-(100*cp_sim_words/cp_diac)

    def wer1_Fmeasure(self,corpus,test):
        recall = self.wer1_Recall(corpus,test)
        precision = self.wer1_Precision(corpus,test)
        if (recall+precision) == 0 : return 0
        return 2*recall*precision/(recall+precision)

    
    
    
    def wer2_Recall(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        cp_sim_words = 0
        cp_words = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                wo1 = self.LettersDiac(words1[j])
                wo2 = self.LettersDiac(words2[j])
                
                wo1 = ''.join(wo1[:len(wo1)-1])
                wo2 = ''.join(wo2[:len(wo2)-1])
                
                
                if self.HasDiac(wo2) and wo1 == wo2: cp_sim_words += 1
                cp_words += 1
        if cp_words == 0 : return 0
        
        return 100-(100*cp_sim_words/cp_words)

    def wer2_Precision(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        cp_sim_words = 0
        cp_diac = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                wo1 = self.LettersDiac(words1[j])
                wo2 = self.LettersDiac(words2[j])
                
                wo1 = ''.join(wo1[:len(wo1)-1])
                wo2 = ''.join(wo2[:len(wo2)-1])
                if self.HasDiac(wo2) and wo1 == wo2: cp_sim_words += 1
                if self.HasDiac(wo2) : cp_diac += 1
        if cp_diac == 0 : return 0
        return 100-(100*cp_sim_words/cp_diac)

    def wer2_Fmeasure(self,corpus,test):
        recall = self.wer2_Recall(corpus,test)
        precision = self.wer2_Precision(corpus,test)
        if (recall+precision) == 0 : return 0
        return 2*recall*precision/(recall+precision)
##################################################################   
    def der1_Recall(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')

        cp_sim_letters = 0
        cp_letters = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                letters1 = self.LettersDiac(words1[j])
                letters2 = self.LettersDiac(words2[j])
                for k in range(len(letters1)):
                    if letters1[k] == letters2[k]: cp_sim_letters += 1
                    cp_letters += 1
        if cp_letters == 0 : return 0
        return 100-(100*cp_sim_letters/cp_letters)

    def der1_Precision(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')

        cp_sim_letters = 0
        cp_diac = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                letters1 = self.LettersDiac(words1[j])
                letters2 = self.LettersDiac(words2[j])
                for k in range(len(letters1)):
                    #pprint(letters1[k]+' == '+letters2[k])
                    if letters1[k] == letters2[k]: cp_sim_letters += 1
                    if self.HasDiac(letters2[k]) : cp_diac += 1
        if cp_diac == 0 : return 0
 
        return 100-(100*cp_sim_letters/cp_diac)

    def der1_Fmeasure(self,corpus,test):
        recall = self.der1_Recall(corpus,test)
        precision = self.der1_Precision(corpus,test)
        if (recall+precision) == 0 : return 0
        return 2*recall*precision/(recall+precision)
    
    
    

    
    
    def der2_Recall(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')

        cp_sim_letters = 0
        cp_letters = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            
            for j in range(len(words1)):
                
                wo1 = self.LettersDiac(words1[j])
                wo2 = self.LettersDiac(words2[j])
                
                wo1 = ''.join(wo1[:len(wo1)-1])
                wo2 = ''.join(wo2[:len(wo2)-1])
                
                letters1 = self.LettersDiac(wo1)
                letters2 = self.LettersDiac(wo2)
                for k in range(len(letters1)):
                    if letters1[k] == letters2[k]: cp_sim_letters += 1
                    cp_letters += 1
        if cp_letters == 0 : return 0
        return 100-(100*cp_sim_letters/cp_letters)

    def der2_Precision(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')

        cp_sim_letters = 0
        cp_diac = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            for j in range(len(words1)):
                
                wo1 = self.LettersDiac(words1[j])
                wo2 = self.LettersDiac(words2[j])
                
                wo1 = ''.join(wo1[:len(wo1)-1])
                wo2 = ''.join(wo2[:len(wo2)-1])
                
                letters1 = self.LettersDiac(wo1)
                letters2 = self.LettersDiac(wo2)
                for k in range(len(letters1)):
                    #pprint(letters1[k]+' == '+letters2[k])
                    if letters1[k] == letters2[k]: cp_sim_letters += 1
                    if self.HasDiac(letters2[k]) : cp_diac += 1
        if cp_diac == 0 : return 0
 
        return 100-(100*cp_sim_letters/cp_diac)

    def der2_Fmeasure(self,corpus,test):
        recall = self.der2_Recall(corpus,test)
        precision = self.der2_Precision(corpus,test)
        if (recall+precision) == 0 : return 0
        return 2*recall*precision/(recall+precision)
##########################################################
    def EvaluateByWord(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        cp_sim_words = 0
        cp_sim_sents = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            cp_sim_words = 0
            for j in range(len(words1)):
                if words1[j] == words2[j]: cp_sim_words += 1
            cp_sim_sents += cp_sim_words/len(words1)
        return cp_sim_sents/len(corpus_sents)

    def EvaluateByChar(self,corpus,test):
        corpus_sents = corpus.strip().split('\n')
        test_sents = test.strip().split('\n')
        similar = 0
        cp_sim_sents = 0
        cp_sim_words = 0
        cp_sim_word = 0
        for i in range(len(corpus_sents)):
            words1 = corpus_sents[i].strip().split(" ")
            words2 = test_sents[i].strip().split(" ")
            cp_sim_words = 0
            for j in range(len(words1)):
                char_word1 = list(words1[j])
                char_word2 = list(words2[j])
                cp_sim_word = 0
                s = 0
                for k in range(len(char_word1)) :
                    if s < len(char_word2):
                        if char_word1[k] not in self.diac and char_word2[s] not in self.diac:
                            if char_word1[k] == char_word2[s]:
                                cp_sim_word += 1
                                s += 1
                        else :
                            if char_word1[k] == char_word2[s]:
                                cp_sim_word += 1
                                s += 1

                cp_sim_words += cp_sim_word / len(char_word1)
            cp_sim_sents += cp_sim_words / len(words1)
        return (cp_sim_sents / len(corpus_sents))*100
