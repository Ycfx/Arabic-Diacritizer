__author__ = 'Youcef'
from tashkeel.handlers.DBHandler import DBHandler
from tashkeel.handlers.MyToolKit import MyToolKit
import time,math,pprint,re
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
        for sent in tool.sents(text.strip(),["\n","\r",".",":",",",';'],subsent=['"',"'",'-']):
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

        ###################### Vocalisation by word #########################
        
        for sent in tool.sents(text.strip(),["\n","\r",".",":",",",';'],subsent=['"',"'",'-']):
            #le replace a revoir, car il change un peut les mots (tatwil)
            sent = "# "+tool.normalizeArabicAlif(tool.DeleteDiacritic(sent)).replace('ـ','')+" $"
            list_words = tool.words(sent)

            #Récuperer les possibilités pour chaque mot
            dict = {}
            for word in list_words:
                res = hdb.SelectOne('dictionary','type="'+word+'"',attribute='vocabularies')
                if res == None: dict[word] = word
                else : dict[word] = res[0]
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
            
        
        #######################################################################
        
        ###################### Vocalisation by letter #########################
        result_teshkeel = self.LettersVocaliser(result_teshkeel,smooth_const)
        #######################################################################
            
            
        result['result'] = result_teshkeel
        result['time'] = round(time.time() - t1,2)
        return result

    
    def getNotVocalised(self,sents):
        tool = MyToolKit()
        not_vocalised_by_sents = []
        for i in range(len(sents)):
            not_vocalised = []
            words = tool.words(sents[i])
            j = 0
            while j < len(words):
                if not tool.HasDiac(words[j]):
 
                    string = ""
                    if j == 0 : string = '###'+words[j]
                    else : 
                        char = tool.LettersDiac(words[j-1])
                        string = char[len(char)-2]+char[len(char)-1]+'#'+words[j]
                    k = j+1
                    while k < len(words) and not tool.HasDiac(words[k]):
                        string += "#"+words[k]
                        k+=1
                    j += k
                    not_vocalised.append(string+"#")
                else : j += 1
            not_vocalised_by_sents.append(not_vocalised)
        return not_vocalised_by_sents
    
    def LettersVocaliser(self,sents,smooth_const):
        tool = MyToolKit()
        hdb = DBHandler('data/model.db')
        hdb.connect()
        res = hdb.getFromTable('letters_dictionary',attribute='type,vocabularies')
        dict = {}
        for r in res: dict[r[0]] = r[1]
    
        
        not_vocalised = self.getNotVocalised(sents)
        pprint("Nombre de non vocalised : "+str(len(not_vocalised)))
        #parcourir les phrases
        for i in range(len(sents)):
            #pprint(not_vocalised[i])
    
            #parcourir les chaines non vocalisé dans une phrase
            for j in range(len(not_vocalised[i])):
                matrice = []
                char = tool.LettersDiac(not_vocalised[i][j])
                list_dict = []
                list_dict.append([-1,tool.HideChar(char[0],expect=['#',' ']),1])
                matrice.append(list_dict)
                
                list_dict = []
                list_dict.append([0,tool.HideChar(char[1],expect=['#',' ']),1])
                matrice.append(list_dict)
                
                list_dict = []
                list_dict.append([0,"#",1])
                matrice.append(list_dict)
                
                string = tool.DeleteDiacritic(not_vocalised[i][j])
                #pprint(string)
                #parcourir les caractéres
         
                #if(string[0] == 'ا' and string[1] == 'ل')
                k = 3
                while k < len(string):
                    list_dict = []
                    if string[k-1] == "#" and string[k] == 'ا' and string[k+1] == 'ل':
                        list_dict = []
                        list_dict.append([0,'_',1])
                        matrice.append(list_dict)
          
                        list_dict = []
                        list_dict.append([0,'_ْ',1])
                        matrice.append(list_dict)
    
                        k += 2
                    else :
                        #parcourir les possibilités
                        for possib in tool.words(dict[string[k]]):
                            if possib == "#":list_dict.append([-1,possib,1])
                            else : list_dict.append([-1,tool.HideChar(possib,expect=['#',' ']),0])
                        matrice.append(list_dict)
                        k += 1
                    

                v = self.ViterbiLetter(matrice,smooth_const)
                string = self.alignLetter(v,not_vocalised[i][j])
                #pprint(string)
                #pprint(not_vocalised[i][j])
                #pprint(sents[i])
                #not_vocalised[i] = not_vocalised[i].replace(not_vocalised[i][j],string)
                sents[i] = sents[i].replace(not_vocalised[i][j].replace('#',' ').strip(),string.replace('#',' ').strip())
                """
                if v[:2] == "##" : n = 0
                else: n = 1
                
                string1 = re.sub('#+',' ',not_vocalised[i][j]).strip().split(' '))
                string2 = re.sub('#+',' ',v).strip().split(' ')
                pprint([0])
                pprint(string)
                pprint('------------')
                """
                #print(not_vocalised[i][j]+' => '+v)
                #exit()
                #pprint('---------------------------------')
                #pprint(matrice)
                """
                for a in matrice:
                    #matrice[i-1][k][1]
                    pprint(a[0][0])
            
                exit()
                """
            
        return sents

    def alignLetter(self,string1,string2):
        tool = MyToolKit()
        diac = ['َ','ِ','ً','ٌ','ٍ','ْ','ّ','ُ']
        string2 = tool.DeleteDiacritic(string2)
        lenth2 = len(string2)
        i = 0
        while i < lenth2:
            if string2[i] != '#': string1 = string1.replace('_',string2[i],1)            
            i += 1
        return string1
        

    def ViterbiLetter(self,matrice,smooth_const):
        V = 426
        e = 0
        for i in range(3,len(matrice)):
            lenPred = len(matrice[i-1])
            for j in range(len(matrice[i])):

                max_ind = 0
                max_val = 0
                for k in range(lenPred):
                    try:
                        p1 = matrice[i-1][k][1]
                        p2 = matrice[i-2][matrice[i-1][k][0]][1]
                        p3 = matrice[i-3][matrice[i-2][k][0]][1]
             
                        #p = math.exp(math.log(self.LaplaceSmoothing_letters(matrice[i][j][1],p3+p2+p1,smooth_const,V))+math.log(matrice[i-1][k][2]))
                        p = math.exp(math.log(self.AbsoluteDiscountingSmoothing_letters(p3+p2+p1,matrice[i][j][1],smooth_const,V))+math.log(matrice[i-1][k][2]))
                    except Exception as exception :
                        #print("#Error log(0) : %s " % exception.args[0])
                        e += 1
                    if p > max_val :
                        max_val = p
                        max_ind = k
                matrice[i][j][0] = max_ind
                matrice[i][j][2] = max_val
            i+=1
        result = ''
        i = 0
        #pprint(matrice)
        #exit()
        for x in matrice[ ::-1]:
            result = x[i][1]+result
            i = x[i][0]

        return result
    
    def Viterbi(self,matrice,smooth_const):
        V = 217847
        for i in range(1,len(matrice)):
            lenPred = len(matrice[i-1])
            for j in range(len(matrice[i])):
                max_ind = 0
                max_val = 0
                for k in range(lenPred):
                    try:
                        #p = math.exp(math.log(self.LaplaceSmoothing(matrice[i][j][1],matrice[i-1][k][1],smooth_const,V))+math.log(matrice[i-1][k][2]))
                        p = math.exp(math.log(self.AbsoluteDiscountingSmoothing(matrice[i][j][1],matrice[i-1][k][1],smooth_const,V))+math.log(matrice[i-1][k][2]))
                    except Exception as exception :
                        print("#Error log(0) : %s " % exception.args[0])
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

    def sentProbaility(self,sent,smooth_const):
        V = 217847
        tool = MyToolKit()
        bigrs = bigrams(tool.words(sent));
        p = 1
        for tuple in bigrs:
            p = math.exp(math.log(p)+math.log(self.LaplaceSmoothing(tuple[1],tuple[0],smooth_const,V)))
            #p = math.exp(math.log(p)+math.log(self.AbsoluteDiscountingSmoothing(tuple[1],tuple[0],smooth_const,V)))
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
        return (count_w1_w2+u)/(count_w2+v*u)

    def AbsoluteDiscountingSmoothing(self,w2,w1,d,v):        
        
        hdb = DBHandler('data/model.db')
        hdb.connect()
        count_w1 = hdb.SelectOne('words','word="'+w1+'"',attribute='freq')
        #count_w2 = hdb.SelectOne('words','word="'+w2+'"',attribute='freq')
        count_w1_w2 = hdb.SelectOne('grams2','grams="'+w1+' '+w2+'"',attribute='freq')
        count_w_w1 = hdb.SelectOne('abs_words','word="'+w1+'"',attribute='freq')
        
        if count_w1 != None: count_w1 = count_w1[0]
        else : count_w1 = 0
        
        """
        if count_w2 != None: count_w2 = count_w2[0]
        else : count_w2 = 0
        """
        if count_w1_w2 != None: count_w1_w2 = count_w1_w2[0]
        else : count_w1_w2 = 0

        if count_w_w1 != None: count_w_w1 = count_w_w1[0]
        else : count_w_w1 = 0
        if count_w1 == 0 : return 0

        return (max([count_w1_w2-d,0])/count_w1)+(d*count_w_w1*(1/v))/count_w1
 
        
        
        
        
        
        
    def AbsoluteDiscountingSmoothing_letters(self,w2,w1,d,v):
        hdb = DBHandler('data/model.db')
        hdb.connect()
        count_w1 = hdb.SelectOne('temp_letters','letter="'+w1+'"',attribute='freq')
        #count_w2 = hdb.SelectOne('words','word="'+w2+'"',attribute='freq')
        count_w1_w2 = hdb.SelectOne('letters_grams3','grams="'+w1+w2+'"',attribute='freq')
        count_w_w1 = hdb.SelectOne('abs_letters','letter="'+w1+'"',attribute='freq')
        
        if count_w1 != None: count_w1 = count_w1[0]
        else : count_w1 = 0

        if count_w1_w2 != None: count_w1_w2 = count_w1_w2[0]
        else : count_w1_w2 = 0

        if count_w_w1 != None: count_w_w1 = count_w_w1[0]
        else : count_w_w1 = 0
        if count_w1 == 0 : return 0

        return (max([count_w1_w2-d,0])/count_w1)+(d*count_w_w1*(1/v))/count_w1 
           
        
        
        
        
    def LaplaceSmoothing_letters(self,w1,w2,u,v):
        hdb = DBHandler('data/model.db')
        hdb.connect()
        
        count_w1 = hdb.SelectOne('temp_letters','letter="'+w1+'"',attribute='freq')
        if count_w1 != None: count_w1 = count_w1[0]
        else : count_w1 = 0
        
        count_w2 = hdb.SelectOne('letters_grams3','grams="'+w2+'"',attribute='freq')
        if count_w2 != None: count_w2 = count_w2[0]
        else : count_w2 = 0
        #pprint('phase 1 : '+w2+' | '+str(count_w2));
        
        count_w1_w2 = hdb.SelectOne('letters_grams4','grams="'+w2+w1+'"',attribute='freq')
        if count_w1_w2 != None: count_w1_w2 = count_w1_w2[0]
        else : count_w1_w2 = 0
        #pprint('phase 2 : '+w2+''+w1+' | '+str(count_w1_w2));
        #Probleme de zero , avec la matrice d'emission(*count_w1)
        return ((count_w1_w2+u)/(count_w2+v*u))