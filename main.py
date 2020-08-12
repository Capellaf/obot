from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
#from flask_ngrok import run_with_ngro
import brain

#Criando servidor flask e iniciando ngrok
app = Flask(__name__) #Servidor flask
#run_with_ngrok(app) #tunnel ngrok

#Rotina a executar quando receber mensagem
@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    user_number = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    response = brain.botresponse(incoming_msg)
    if resp != False:
        msg.body(response)
        responded = True
    else:
        msg.body("I don’t have an answer for it now. But we’ll get one ASAP")
        responded = True
    if not responded:
        msg.body("There are some keywords to help:\n*Tell me about* - Use to discover about something. Example: Tell me about space\n*Ask me something* - I ask you something to start a conversation\n*How can I say* - Use to discover how to say something in english. Example: How can I say hoje está calor\n*Translate* - Translate something to portuguese\n*What means* - Use to search a word in english dictionary\n*Give me some tip* - Use to get some tips about speak english\n*Give me some dialogue -* Use to get some dialogue example\n*Give me some word -* Use to get a random word to improve your vocabulary\n*Give me some expression:* Use to get a random expression\n*How's the weather in:* Use to get the weather conditions about some city. You need to tell de city and the country abreviation. Example: How's the weather in São Paulo BR?\n*Note:* Use to send a message to my programmer.\n*Help* - Use if you forget these keywords\n\n*I'm still learning, help me to improve, get your feedback*")
        responded = True
    return str(resp)

#Executando o app Flask
if(__name__) == '__main__':
    app.run()
