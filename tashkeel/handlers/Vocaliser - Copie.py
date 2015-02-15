__author__ = 'Youcef'
from tashkeel.handlers.DBHandler import DBHandler
from tashkeel.handlers.MyToolKit import MyToolKit
import time,math,pprint
from nltk.util import bigrams
from pprint import pprint
class Vocaliser:

    def moushakeel_V1(self,text,smooth_const):
        t1 = time.time()
        tool = MyToolKit()
        hdb = DBHandler('data/model.db')
        result = {}
        hdb.connect()
        result_teshkeel = []
        result['token'] = 0
        result['type'] = 0
        #paragComp = tool.sents(text.strip(),["\n","\r",".",":",",",';'],subsent=['"',"'",'-']);
        paragComp = tool.sents(text.strip(),["\n","\r",".",":",",",';']);
        for sent in paragComp[0]:
            text = "# "+tool.normalizeArabicAlif(tool.DeleteDiacritic(sent))+" $"
            list_words = tool.words(text)
            #Récuperer les possibilités pour chaque mot
            dict = {}
            for word in list_words:
                res = hdb.SelectOne('dictionary','type="'+word+'"',attribute='vocabularies')
                if res == None: dict[word] = word
                else : dict[word] = res[0]
            dict['#'] = '#'
            dict['$'] = '$'
            possibilities = self.getPossibilities(list_words,dict)
            max_p = 0
            best_sent = ''
            for possib in possibilities:
                p = self.sentProbaility(possib,smooth_const)
                if p > max_p :
                    p = max_p
                    best_sent = possib
            result_teshkeel.append(' '.join(tool.words(best_sent)[1:len(tool.words(best_sent))-1]))
            result['token'] = len(list_words)-2
            result['type'] = len(dict)-2
        result['result'] = result_teshkeel
        result['time'] = round(time.time() - t1,2)
        return result

    def moushakeel_V2(self,text,smooth_const):
        t1 = time.time()
        tool = MyToolKit()
        hdb = DBHandler('data/model.db')
        result = {}
        hdb.connect()
        result_teshkeel = []
        result['token'] = 0
        result['type'] = 0

        #paragComp = tool.sents(text.strip(),["\n","\r",".",":",",",';'],subsent=['"',"'",'-']);
        paragComp = tool.sents(text.strip(),["\n","\r",".",":",",",';']);
        #pprint(paragComp[1])
        #not_vocalised_by_sents = []
        
        for sent in paragComp[0]:
            #not_vocalised = []
            sent = "# "+tool.normalizeArabicAlif(tool.DeleteDiacritic(sent))+" $"
            list_words = tool.words(sent)
            #Récuperer les possibilités de vocalisation pour chaque mot
            dict = {}
            #prev = ""
            for word in list_words:
                    
                res = hdb.SelectOne('dictionary','type="'+word+'"',attribute='vocabularies')
                if res == None: 
                    dict[word] = word
                    #not_vocalised.append((word,prev))
                else : dict[word] = res[0]
                #prev = word
            dict['#'] = '#'
            dict['$'] = '$'
            #HMM
            matrice = []
            for word in list_words:
                list_dict = []
                for possib in tool.words(dict[word]):
                    if possib == "#":list_dict.append([-1,possib,1])
                    else : list_dict.append([-1,possib,0])
                matrice.append(list_dict)

            sent = self.Viterbi(matrice,smooth_const)
            result_teshkeel.append(' '.join(tool.words(sent)[1:len(tool.words(sent))-1]))
            result['token'] += len(list_words)-2
            result['type'] += len(dict)-2
            #not_vocalised_by_sents.append(not_vocalised)
         
    

     
        #pprint(not_vocalised_by_sents)
        
        #pprint(result_teshkeel)
        #result_teshkeel = paragComp[0]
        result_teshkeel = self.VocalizeLetters(result_teshkeel,smooth_const)
        result['result'] = result_teshkeel
        result['time'] = round(time.time() - t1,2)
        return result

    def VocalizeLetters(self,sents,smooth_const):
        tool = MyToolKit()
        
        hdb = DBHandler('data/model.db')
 
        hdb.connect()
        dict = {}
        res = hdb.getFromTable('letters_dictionary',attribute='type,vocabularies')
        for r in res:
            dict[r[0]] = r[1]
        for i in range(len(sents)):
            #pprint("La phrase : "+sents[i])
            list_words = tool.words(sents[i])
            prev = ""
            not_vocalised = []
            
            for word in list_words:
                if not tool.HasDiac(word):
                    """
                    a = tool.DeleteDiacritic(prev)
                    not_vocalised.append(a[len(a)-1]+' '+word)
                    """
                    #not_vocalised.append('#'+word+'#')
                    a = tool.DeleteDiacritic(prev)
                    #Condition qui vérifier si le mot précédent a un nombre de caractere inferieure a 3
                    pprint("Lennnn : "+str(len(a)))
     
                    if(len(a) == 0): pred = "##"
                    elif(len(a) == 1): pred = a[len(a)-1]+"#"
                    else : pred = a[len(a)-2]+a[len(a)-1]
                    not_vocalised.append(pred+'#'+word+"#")
                prev = word
            #pprint('-----------------')
 
                
            for j in range(len(not_vocalised)):
                pprint("---"+not_vocalised[j])
                matrice = []
                
                
                
                list_dict = []
                list_dict.append([-1,self.HideChar(not_vocalised[j][0]),1])
                matrice.append(list_dict)
                list_dict = []
                list_dict.append([-1,self.HideChar(not_vocalised[j][1]),1])
                matrice.append(list_dict)
                
                
                
                for k in range(2,len(not_vocalised[j])):
                    pprint("Letter : "+not_vocalised[j][k])
                    #exit()
                    list_dict = []
                    if not_vocalised[j][k] != "#": 
                        #pprint('ici')
                        #pprint(dict[letter])
                        for possib in dict[not_vocalised[j][k]].split(): 
                            #list_dict.append([-1,self.HideChar(possib),0])
                            list_dict.append([-1,possib,0])
                        
                    else: list_dict.append([-1,"#",1]);
                    matrice.append(list_dict)
                    #pprint(matrice)
               
                #not_vocalised[j] = Viterbi_letters(matrice,smooth_const)
                
                a = self.Viterbi_letters(matrice,smooth_const,not_vocalised[j][:2])
                pprint("tashkeel : ("+a.strip()+") => ("+not_vocalised[j].strip()+")")
                #pprint('---'+sents[i])
                sents[i] = sents[i].replace(not_vocalised[j].replace('#',''), a.replace('#',''))
          
            #pprint(not_vocalised)
        return sents
  
    
    def Viterbi(self,matrice,smooth_const):
        V = 217847
        error = 0
        for i in range(1,len(matrice)):
            lenPred = len(matrice[i-1])
            for j in range(len(matrice[i])):
                max_ind = 0
                max_val = 0
                for k in range(lenPred):
                    try:
                        
                        p = math.exp(math.log(self.LaplaceSmoothing(matrice[i][j][1],matrice[i-1][k][1],smooth_const,V))+math.log(matrice[i-1][k][2]))
                        #p = math.exp(math.log(self.AbsoluteDiscountingSmoothing(matrice[i][j][1],matrice[i-1][k][1],0.75,V))+math.log(matrice[i-1][k][2]))
                    except Exception as exception :
                        pprint('ici')
                        error += 0
                        
                        #print("#Error log(0) : %s " % exception.args[0])
                    if p > max_val :
                        max_val = p
                        max_ind = k
                matrice[i][j][0] = max_ind
                matrice[i][j][2] = max_val
            i+=1
        result = ''
        i = 0
        #pprint(matrice)
        for x in matrice[ ::-1]:
            result = x[i][1]+' '+result
            i = x[i][0]

        return result

    
    
    def Viterbi_letters(self,matrice,smooth_const,pred):
        V = 426
        error = 0
        for i in range(1,len(matrice)):
            lenPred = len(matrice[i-1])
            for j in range(len(matrice[i])):
                max_ind = 0
                max_val = 0
                for k in range(lenPred):
                    try:
                        if(i-1 == 0) : a = matrice[i-1][k][1]+pred[1]+pred[0]
                        elif(i-1 == 1): a = matrice[i-1][k][1]+matrice[i-2][k][1]+pref[1]
                        else : a = matrice[i-1][k][1]+matrice[i-2][k][1]+matrice[i-3][k][1]
                        
                        
                        p = math.exp(math.log(self.LaplaceSmoothing_letters(matrice[i][j][1],a,smooth_const,V))+math.log(matrice[i-1][k][2]))
                        #p = math.exp(math.log(self.AbsoluteDiscountingSmoothing(matrice[i][j][1],matrice[i-1][k][1],0.75,V))+math.log(matrice[i-1][k][2]))
                    except Exception as exception :
                        error += 0
                        
                        #print("#Error log(0) : %s " % exception.args[0])
                    if p > max_val :
                        max_val = p
                        max_ind = k
                matrice[i][j][0] = max_ind
                matrice[i][j][2] = max_val
            i+=1
        result = ''
        i = 0
        pprint(matrice)
        for x in matrice[ ::-1]:
            result = x[i][1]+result
            i = x[i][0]

        return result
    ###################################

    ###################################
    def sentProbaility(self,sent,smooth_const):
        V = 217847
        tool = MyToolKit()
        bigrs = bigrams(tool.words(sent));
        p = 1
        for tuple in bigrs:
            p = math.exp(math.log(p)+math.log(self.LaplaceSmoothing(tuple[1],tuple[0],smooth_const,V)))
            #p = math.exp(math.log(p)+math.log(self.AbsoluteDiscountingSmoothing(tuple[1],tuple[0],0.75,V)))
        return p

    def getPossibilities(self,list_words,dict):
        tool = MyToolKit()
        possibilities = []
        i = 1
        lenList = len(list_words)
        possibilities.append(list_words[0])
        lenpred = 1
        while len(tool.words(possibilities[0]))<lenList:
            first = possibilities[0]
            if len(tool.words(first)) != lenpred:
                i += 1
                lenpred = len(tool.words(first))
            for word in tool.words(dict[list_words[i]]):
                possibilities.append(first+" "+word)
            possibilities.pop(0)
        return possibilities

    def LaplaceSmoothing(self,w2,w1,u,v):
        hdb = DBHandler('data/model.db')
        hdb.connect()
        count_w2 = hdb.SelectOne('words','word="'+w2+'"',attribute='freq')
        if count_w2 != None: count_w2 = count_w2[0]
        else : count_w2 = 0

        count_w1_w2 = hdb.SelectOne('grams2','grams="'+w1+' '+w2+'"',attribute='freq')
        if count_w1_w2 != None: count_w1_w2 = count_w1_w2[0]
        else : count_w1_w2 = 0
        return (count_w1_w2+u)/((count_w2+v)*u)
    
    
    
    def LaplaceSmoothing_letters(self,w1,w2,u,v):
        hdb = DBHandler('data/model.db')
        hdb.connect()
        
        count_w1 = hdb.SelectOne('letters','letter="'+w1+'"',attribute='freq')
        if count_w1 != None: count_w1 = count_w1[0]
        else : count_w1 = 0
        pprint('phase 1 : '+w2);
        count_w2 = hdb.SelectOne('letters_grams3','grams="'+w2+'"',attribute='freq')
        if count_w2 != None: count_w2 = count_w2[0]
        else : count_w2 = 0
        pprint('phase 2 : '+w2+' '+w1);
        count_w1_w2 = hdb.SelectOne('letters_grams4','grams="'+w2+'#'+w1+'"',attribute='freq')
        if count_w1_w2 != None: count_w1_w2 = count_w1_w2[0]
        else : count_w1_w2 = 0
            
        return ((count_w1_w2+u)/((count_w2+v)*u))

   