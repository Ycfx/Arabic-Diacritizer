import json,re,nltk
from django.http import HttpResponse
from django.template import RequestContext, loader
import math
from tashkeel.handlers.DBHandler import DBHandler
from tashkeel.handlers.MyToolKit import MyToolKit
from tashkeel.handlers.Vocaliser import Vocaliser
from pprint import pprint
import time,random

def index(request):
    template = loader.get_template('home.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def DeletDiac(request):
    t1 = time.time()
    tool = MyToolKit()
    result = {}
    res = []
    
    for sent in tool.sents(request.POST['text'].strip(),["\n","\r",".",":",",",';'],subsent=['"',"'",'-'])[0]:
        res.append(tool.DeleteDiacritic(sent))
    result['results'] = '<br>'.join(res)
    result['time'] = round(time.time() - t1,2)
    return HttpResponse(json.dumps(result),content_type="application/json")

def getdict(request):
    t1 = time.time()
    tool = MyToolKit()
    hdb = DBHandler('data/model.db')
    hdb.connect()
    result = {}
    dict = {}
    text = tool.DeleteDiacritic(tool.normalizeArabicAlif(request.POST['text'].strip()))
    list_words = tool.words(text)
    for word in list_words:
        res = hdb.SelectOne('dictionary','type="'+word+'"',attribute='vocabularies')

        if res == None: dict[word] = ''
        else : dict[word] = re.sub(' ','  -  ',res[0])
    result['results'] = dict
    result['time'] = round(time.time() - t1,2)
    result['type'] = len(dict)
    result['token'] = len(list_words)
    return HttpResponse(json.dumps(result),content_type="application/json")

def tashkeel_v1(request):
    vocaliser = Vocaliser()
    result = vocaliser.moushakeel_V1(request.POST['text'],float(request.POST['ConstLaplace']))
    result['result'] = '<br>'.join(result['result'])
    return HttpResponse(json.dumps(result),content_type="application/json")

def tashkeel_v2(request):
    vocaliser = Vocaliser()
    result = vocaliser.moushakeel_V2(request.POST['text'],float(request.POST['ConstLaplace']))
    result['result'] = '<br>'.join(result['result'])
    return HttpResponse(json.dumps(result),content_type="application/json")

def GetTestSents(request):
    nbr =  request.POST['nbrTestSents'].strip()
    if nbr != "":
        try:
            tool = MyToolKit()
            hdb = DBHandler('data/model.db')
            result = {}
            hdb.connect()
            cond = ' '
            for i in range(int(nbr)):
                if i < int(nbr)-1 : cond += "id="+str(random.randint(1,36111))+" or "
                else : cond += "id="+str(random.randint(1,36111))

            DataSents = hdb.getFromTable('sents_test',attribute='sent',condition=cond)

            #pprint(sents)
            sents_diac = ''
            for sent in DataSents:
                sents_diac += ' '.join(tool.words(sent[0])[1:len(tool.words(sent[0]))-1])+'\n'
            sents = tool.DeleteDiacritic(sents_diac)
            result['sents_diac'] =  sents_diac
            result['sents_whitout_diac'] = sents

        except ValueError: result = None
        #r = random.randint(1,100)
    else : result = None
    return HttpResponse(json.dumps(result),content_type="application/json")

def Evaluate(request):
    t1 = time.time()
    tool = MyToolKit()

    text =  request.POST['text'].strip()
    corpus_text = request.POST['sents_diac_corpus_value'].strip()
    result = {}
    result['recall'] = "{:.4f}".format(tool.Recall(corpus_text,text))
    result['precision'] = "{:.4f}".format(tool.Precision(corpus_text,text))
    result['fmeasure'] ="{:.4f}".format(tool.Fmeasure(corpus_text,text))#2*result['recall']*result['precision']/(result['precision']+result['precision'])

    result['time'] = round(time.time() - t1,2)
    return HttpResponse(json.dumps(result),content_type="application/json")

def TashkeelAndEvaluate(request):
    vocaliser = Vocaliser()
    tool = MyToolKit()
    text =  request.POST['text'].strip()
    corpus_text = request.POST['sents_diac_corpus_value'].strip()
    result = vocaliser.moushakeel_V2(text,float(request.POST['ConstLaplace']))
    joined_result = '\n'.join(result['result'])
    result['wer1_recall'] = "{:.4f}".format(tool.wer1_Recall(corpus_text,joined_result))
    result['wer1_precision'] = "{:.4f}".format(tool.wer1_Precision(corpus_text,joined_result))
    result['wer1_fmeasure'] = "{:.4f}".format(tool.wer1_Fmeasure(corpus_text,joined_result))#2*result['recall']*result['precision']/(result['precision']+result['precision'])
    
    result['wer2_recall'] = "{:.4f}".format(tool.wer2_Recall(corpus_text,joined_result))
    result['wer2_precision'] = "{:.4f}".format(tool.wer2_Precision(corpus_text,joined_result))
    result['wer2_fmeasure'] = "{:.4f}".format(tool.wer2_Fmeasure(corpus_text,joined_result))#2*result['recall']*result['precision']/(result['precision']+result['precision'])
     
    result['der1_recall'] = "{:.4f}".format(tool.der1_Recall(corpus_text,joined_result))
    result['der1_precision'] = "{:.4f}".format(tool.der1_Precision(corpus_text,joined_result))
    result['der1_fmeasure'] = "{:.4f}".format(tool.der1_Fmeasure(corpus_text,joined_result))#2*result['recall']*result['precision']/(result['precision']+result['precision'])

    result['der2_recall'] = "{:.4f}".format(tool.der2_Recall(corpus_text,joined_result))
    result['der2_precision'] = "{:.4f}".format(tool.der2_Precision(corpus_text,joined_result))
    result['der2_fmeasure'] = "{:.4f}".format(tool.der2_Fmeasure(corpus_text,joined_result))#2*result['recall']*result['precision']/(result['precision']+result['precision'])
     
    
    result['result'] = '<br>'.join(result['result'])
    return HttpResponse(json.dumps(result),content_type="application/json")


