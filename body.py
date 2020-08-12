import wikipediaapi
import string
import random
from datetime import datetime
from PyDictionary import PyDictionary
from googletrans import Translator
from os import walk
import os
import emojis
import pyowm
from pyowm import OWM

dictionary = PyDictionary() #Dicionário
translator = Translator() # Tradutor
owm = OWM('8d7f66bc77243899a96e5ed130e400d2')
mgr = owm.weather_manager()

def getnote(incoming_msg): #Função para armazenar nota
    f = open('notes.txt', 'a')
    text = incoming_msg.replace('note:','')
    f.write(text+'\n')
    f.close()
    return ('Thanks for your feedback!')

def checkemoji(incoming_msg): #Função para verificar emoji
    if ':' in emojis.decode(incoming_msg):
        emj = emojis.decode(incoming_msg)
        emj = emj.replace(':','')
        emjc = emojis.db.get_emoji_by_alias(emj)
        emjc = emjc.category
        emj = emj.replace('_',' ')
        emjs = emj.split()
        lc = len(emjs[0])-1
        if emjc == 'Flags':
            return("This is "+emj)
        elif emjs[0][lc] == 's':
            return("These are the "+emj)
        elif 'men' in emj :
            return("These are "+emj)
        elif emjs[0][0] in "aeio":
            return("This is an "+emj)
        else:
            return("This is a "+emj)
    else:
        return ("Ok")

def getweather(incoming_msg): #Função para verificar clima
    city = incoming_msg.replace("how's","how is")
    city = city.replace("how is the weather in ",'')
    city = city.replace("how is the weather in ",'?')
    city = city.replace(' ',',')
    try:
        mgr.weather_at_place(city)
    except:
        return("I can't find this city")
    else:
        observation = mgr.weather_at_place(city)
        w = observation.weather
        t = w.temperature('celsius')
        wd = w.wind()
        wd = wd['speed']*1.60934
        wd = round(wd,2)
        return('*Status:* '+w.status+'\n*Temperature:* '+str(t['temp'])+'°C\n*Max temperature:* '+str(t['temp_max'])+'°C\n*Min temperature:* '+str(t['temp_min'])+'°C\n*Feels like:* '+str(t['feels_like'])+'°C\n*Wind speed:* '+str(wd)+'km/h\n*Humidity:* '+str(w.humidity)+'%')

def getrandomarchive(folder): #Buscar arquivo aleatório
    files = []
    for (dirpath, dirnames, filenames) in walk('keywords/'+folder):
        files.extend(filenames)
        break
    nr = random.randrange(0, len(files))
    filename = files[nr-1]
    f = open('keywords/'+folder+filename, 'r',encoding="utf8")
    txt = ''.join(f.readlines())
    return (txt)
    f.close()

def getrandomline(archive): #Função linha aleatória em arquivo
    f = open('keywords/'+archive, 'r',encoding="utf8")
    lista = f.readlines()
    nr = random.randrange(0, len(lista))
    line = lista[nr]
    f.close()
    return (line)

def getrandomword(): #Função para buscar palavra aleatória e significado
    sig = None
    while sig == None:
        word = getrandomline('words.txt')
        sig = dictionary.meaning(word)
    f.close()
    return ('Take this one: '+str(word)+'\n\n'+str(sig))

def translate(txt,s,d): #Função para traduzir termo
    tr = translator.translate(txt, src=s, dest=d)
    return ('You could say "'+tr.text+'"')

def searchwikipedia(asking): #Função de pesquisa no wikipedia
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(asking)
    if page.exists():
        info = page.summary[0:1000]
        infotogo = info + '\n\n You can learn more at ' + page.fullurl
    else:
        infotogo = "Sorry, I didn't find anything!"
    return (infotogo)

def greetings(splited,incoming_msg,style): #Função de resposta a comprimento
    if style == 1:
        choicesDoing = ["I'm fine, ","I'm doing great, ","I'm good, ","I'm doing well,"]
        choicesAndyou = ["how about you?","and you?"]
        if 'hey' in splited or 'hi' in splited or 'hello' in splited or 'hey,' in splited or 'hi,' in splited or 'hello,' in splited:
            choicesHi = ['Hi, ','Hello, ','Hey, ']
            greeting = random.choice(choicesHi)+random.choice(choicesDoing)+random.choice(choicesAndyou)
        elif 'good morning' in incoming_msg or 'good afternoon' in incoming_msg or 'good evening' in incoming_msg:
            hr = datetime.now()
            if hr.hour < 12:
                hd = 'Good morning, '
            elif hr.hour < 18:
                hd = 'Good afternoon, '
            else:
                hd = 'Good evening, '
            greeting = hd+random.choice(choicesDoing)+random.choice(choicesAndyou)
        else:
            greeting = random.choice(choicesDoing)+random.choice(choicesAndyou)
        return (greeting)
    elif style == 2:
        hr = datetime.now()
        if hr.hour < 12:
            hd = 'Good morning, '
        elif hr.hour < 18:
            hd = 'Good afternoon, '
        else:
            hd = 'Good evening, '
        choicesGreeting = ["how are you?","how are you today?","how are you doing today?","how is it going?"]
        greeting = hd+random.choice(choicesGreeting)
        return (greeting)
    else:
        choicesHi = ['Hi, ','Hello, ','Hey, ']
        choicesGreeting = ["how are you?","how are you today?","how are you doing today?","how is it going?"]
        greeting = random.choice(choicesHi)+random.choice(choicesGreeting)
        return (greeting)

def findarchives(path): #Função para listar arquivos dentro de pasta
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    return files

def getarchives(path,splited): #Função para procurar diretórios e arquivos
    while (os.path.isdir(path)) == True:
        files = findarchives(path)
        del(splited[0])
        path = (path+'/'+splited[0])
    return (path,splited,files)

def getline(path,term): #Função para buscar linha em arquivo
    f = open(path, 'r')
    found = False
    while found == False:
        line = f.readline().split()
        if line == []:
            term = 'GENERIC'
            f2 = open('noresponse.txt', 'a')
            f2.write(incoming_msg+'\n')
            f2.close()
            f.close()
            f = open(path, 'r')
        elif term == line[0]:
            del(line[0])
            line = ' '.join(line)
            if term == 'GENERIC':
                line = line.split('-')
                line = random.choice(line)
            return (line)
            found = True
            break

def getresponse(verb,splited,incoming_msg): #Função para responder verbos
    #Retira o verbo da string e tudo que tiver anteriormente
    for n in range(len(splited)):
        if splited[n] == verb:
          pos = n
          break
    for n in range(pos+1):
        del(splited[0])
    #Busca subpastas e seleciona a correta
    path = ('rules/'+verb+'/'+splited[0])
    ext = getarchives(path,splited)
    path = ''.join(ext[0]) #Caminho da pasta
    txt = ' '.join(ext[1]) #Texto restante da string
    splited_txt = txt.split() #Texto dividido por palavras
    files = ext[2] #Lista de arquivos na pasta
    path = path.replace(splited_txt[0],'') #Arrumando caminho da pasta
    if '?' in splited_txt[0]:
        removal = splited_txt[0].replace('?','')
        arch = removal+'.txt'
    else:
        arch = splited_txt[0]+'.txt'
    txt = '_'.join(splited_txt)
    if  arch in files:
        new_arch = arch.replace('.txt','?')
        arch = arch.replace('.txt','')
        txt = txt.replace(arch+'_','')
        txt = txt.replace('??','?')
        return(getline(path+arch+'.txt',txt))
    else:
        return(getline(path+'others.txt',txt))
