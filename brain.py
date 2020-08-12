import body

#Rotina a executar quando receber mensagem
def botresponse(incoming_msg):
    if "'" in incoming_msg:
        incoming_msg = incoming_msg.replace("'s",' is')
        incoming_msg = incoming_msg.replace("'d",' would')
        incoming_msg = incoming_msg.replace("'re",' are')
        incoming_msg = incoming_msg.replace("'ve",' have')
        incoming_msg = incoming_msg.replace("'m",' am')
        incoming_msg = incoming_msg.replace("n't",' not')
    elif "’" in incoming_msg:
        incoming_msg = incoming_msg.replace("’s",' is')
        incoming_msg = incoming_msg.replace("’d",' would')
        incoming_msg = incoming_msg.replace("’re",' are')
        incoming_msg = incoming_msg.replace("’ve",' have')
        incoming_msg = incoming_msg.replace("’m",' am')
        incoming_msg = incoming_msg.replace("n’t",' not')
    incoming_msg.replace('type of','typeof')
    incoming_msg.replace('kind of','kindof')
    splited = incoming_msg.split()
    splited.append(None)
    splited.append(None)

    if 'note:' in incoming_msg:
        return (body.getnote(incoming_msg))
    elif "how's the weather in" in incoming_msg or "how is the weather in" in incoming_msg:
        return (body.getweather(incoming_msg))
    elif 'give me some dialogue' == incoming_msg:
        return (body.getrandomarchive('dialogue'))
    elif 'give me some word' == incoming_msg:
        return (body.getrandomword())
    elif 'give me some expression' == incoming_msg:
        return (body.getrandomarchive('expression'))
    elif 'give me some tip' in incoming_msg:
        return (body.getrandomarchive('quick_tips'))
    elif "translate" == splited[0]:
        ph = incoming_msg.replace("translate ", '')
        return(body.translate(ph,'en','pt'))
    elif 'how' == splited[0] and 'can' == splited[1] and 'i' == splited[2] and 'say' == splited[3]:
        ph = incoming_msg.replace("how can i say ", '')
        return(body.translate(ph,'pt','en'))
    elif 'tell' == splited[0] and 'me' == splited[1] and 'about' == splited[2]:
        asking = incoming_msg.replace("tell me about ",'')
        return (body.searchwikipedia(asking))
    elif 'ask' == splited[0] and 'me' == splited[1] and 'something' == splited[2]:
        return(body.getrandomline('askmesomething.txt'))
    elif 'how are you' in incoming_msg:
        return(body.greetings(splited,incoming_msg,1))
    elif "and you?" in incoming_msg or "how about you?" in incoming_msg:
        return ('Same here')
    elif 'good morning' in incoming_msg or 'good afternoon' in incoming_msg or 'good evening' in incoming_msg:
        return(body.greetings(splited,incoming_msg,2))
    elif 'hey' in splited or 'hi' in splited or 'hello' in splited or 'hey,' in splited or 'hi,' in splited or 'hello,' in splited:
        return(body.greetings(splited,incoming_msg,3))
    elif 'rather' in splited:
        choices = ["Whatever","Whatever, I like both","I think the first one is better","Oh, hard decision","Good point, I can't choose"]
        return (random.choice(choices))
    elif 'help' == incoming_msg:
        return ("There are some keywords to help:\n\n*Tell me about* - Use to discover about something. Ex: Tell me about space\n*Ask me something* - I ask you something to start a conversation\n*How can I say* - Use to discover how to say something in english. Example: How can I say hoje está calor\n*Translate* - Translate something to portuguese\n*What means* - Use to search a word in english dictionary\n*Give me some tip* - Use to get some tips about speak english\n*Give me some dialogue:* Use to get some dialogue example\n*Give me some word:* Use to get a random word to improve your vocabulary\n*Give me some expression:* Use to get a random expression\n*How's the weather in:* Use to get the weather conditions about some city. You need to tell the city and de country abreviation. Example: How's the weather in São Paulo BR?\n*Note:* Use to send a message to my programmer\n*Help* - Use if you forget these keywords\n\n*I'm still learning, help me to improve, get your feedback to us!*")
    elif splited[1] == None:
        return(body.checkemoji(incoming_msg))
    else:
        tam = len(splited)
        del(splited[tam-1])
        del(splited[tam-2])
        for i in range(0,len(splited)):
            if os.path.exists('rules/'+splited[i]):
                return body.getresponse(splited[i],splited,incoming_msg)
                break
        return False
