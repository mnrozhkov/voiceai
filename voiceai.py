#BOT and NETWORK LIBs
from flask import Flask, request
from pymessenger.bot import Bot

#NLP LIBs
import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.stanford import StanfordPOSTagger

#SYSTEM LIBs
#import urllib.request
#import json
import os

#MODULE CONTROLS
from loadmusic import MusicControl
from loadtrainer import TrainControl
#from loadbrightness import BrightnessControl
#from loadnet import QuestionControl
#from loadalarm import AlarmControl
#from loadgreet import GreetingControl
from typeclassifier import TypeClassifier

snt = StanfordNERTagger('stanford-ner/voiceai-ner.ser.gz', 'stanford-ner/stanford-ner.jar') 
spt = StanfordPOSTagger('stanford-pos/voiceai-pos.tagger', 'stanford-pos/stanford-postagger.jar')

mp  = MusicControl()
tc  = TrainControl()
#bc  = BrightnessControl()
#qc  = QuestionControl()
#ac  = AlarmControl()
#gc  = GreetingControl()
tyc = TypeClassifier("fastText/voiceai.bin")

prevMessageType = 0

app = Flask(__name__)

ACCESS_TOKEN = "EAADY5DbIKHMBANJuls1tuvUqk9ZA8zdxUsDk2sF3fNR3XfQpvmrwsrIctyNsVkZCakWX4zkELXUgkWYJL7Jvls4KuLZCrr3QtZCmVRHCTv1A8G4bozrsN80hdKuicnk54Hs0N9ieJDQZB4cZAlIYUrKUslpWVFWVO6rPXxfQ8AtgZDZD"
VERIFY_TOKEN = "ironpatriot"
bot = Bot(ACCESS_TOKEN)
recipient_id = None

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        msg = process_message(message)
                        
                        bot.send_text_message(recipient_id, msg)
                    if x['message'].get('attachments'):
                        for att in x['message'].get('attachments'):
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Success"

def process_message(msg):
	msg_words = nltk.word_tokenize(msg)
	original_msg = msg
	#MESSAGE TYPE CLASSIFIERS:
	#1 - Music
	#2 - Brightness and Volume
	#3 - Questions/Google/Wiki
	#4 - Alarm
	#0 - Train POS and NER

	if msg_words == 'xadd' or msg_words == 'xtrain':
		#START TRAINING/ADDING
		return "Train / Add done!"

	textType = tyc.classifyText(msg)
	if textType > -1:
		msg=str(textType)
	else:
		return "I'm sorry I didn't get that, Vidur"

	#CATCH POS
	Nouns = []
	Verbs = []
	Adjs  = []
	entities = []
	pos_tagged = spt.tag(msg_words)
	
	for i, tup in enumerate(pos_tagged):
		mixed = tup[0]+'-'+tup[1]
		msg = msg + ' ' + mixed
		if tup[1] == 'VER':
			Verbs.append((i, tup[0].lower()))
		else:
			if tup[1] == 'ADJ':
				Adjs.append((i, tup[0].lower()))
			else:
				if tup[1] == 'NNN':
					Nouns.append((i, tup[0].lower()))
	
	#CATCH ENTITIES
	entities = []
	ct = -1
	prevEntity = False
	for i, tup in enumerate(pos_tagged):
		if tup[1] == 'ENT':
			if prevEntity == True:
				entities[ct].append(tup[0])
			else:
				ct = ct + 1
				entities.append([])
				entities[ct].append(tup[0])
				prevEntity = True
		else:
			prevEntity = False

	#CATCH ENTITY TYPES
	People = []
	Organisations = []
	Artworks = []
	Locations = []
	Time = []
	Date = []
	Quatity = []
	Money = []
	
	msg = "".join([msg, "\nEntities : "])
	for entity in entities:
		pos_tagged = snt.tag(entity)
		msg2 = " ".join(["-".join([x[0], x[1]]) for x in pos_tagged])
		msg = "\n".join([msg, msg2])
		if pos_tagged[0][1] == 'PER':
			People.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'ART':
			Artworks.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'ORG':
			Organisations.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'LOC':
			Locations.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'TIM':
			Time.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'DAT':
			Date.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'QUA':
			Quantity.append(" ".join([x[0] for x in pos_tagged]))
		if pos_tagged[0][1] == 'MON':
			Money.append(" ".join([x[0] for x in pos_tagged]))

	#SELECT TYPE CONTROL
	
	if textType == 1:
		#TYPE MUSIC
		#Keywords - play, stop, pause, resume, shuffle - VERBS, music, song(s), track(s), artist, singer, musician, album, band - NOUNS, next, previous - ADJS, ART, PER - ENT	

		MusicVerb = ""
		for eachVerb in Verbs:
			verbSub = eachVerb[1].lower()
			if verbSub == 'play' or verbSub == 'stop' or verbSub == 'pause' or verbSub == 'resume' or verbSub == 'shuffle':
				MusicVerb = verbSub
				break

		if MusicVerb == 'stop':
			mp.Stop()
			return msg

		if MusicVerb == 'pause':
			mp.Pause()
			return msg

		if MusicVerb == 'resume':
			msg = "\n".join([msg, "Playing song :", mp.SearchSong()])
			return msg

		Modifier = ""
		for eachAdj in Adjs:
			adjSub = eachAdj[1].lower()
			if adjSub == 'next' or adjSub == 'previous' or adjSub == 'last':
				Modifier = adjSub
				break

		if Modifier == 'next':
			mp.Next()
			return msg

		if Modifier == 'previous' or Modifier == 'last':
			mp.Prev()
			return msg
		
		song_name = None
		artist_name = None
		album_name = None

		if len(People) > 0:
			artist_name = People[0]

		if len(Artworks) > 0:
			song_name = Artworks[0]

		if len(Artworks) > 1:
			album_name = Artworks[1]

		if MusicVerb == 'play':
			msg = "\n".join([msg, "Playing song :", mp.SearchSong(song_name, artist_name, album_name)])
			#bot.send_text_message(recipient_id, msg)

		return msg
	
	if textType == 2:
		return msg

	return msg


if __name__ == "__main__":
    app.run(port=5000, debug=True)
