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
from loadhardware import HardwareControl
#from loadnet import QuestionControl
#from loadalarm import AlarmControl
#from loadgreet import GreetingControl
from typeclassifier import TypeClassifier

class VoiceAIControl(ner_dir, pos_dir, ft_dir):

	self.snt = StanfordNERTagger(ner_dir[0], ner_dir[1])#'stanford-ner/voiceai-ner.ser.gz', 'stanford-ner/stanford-ner.jar') 
	self.spt = StanfordPOSTagger(pos_dir[0], pos_dir[1])#'stanford-pos/voiceai-pos.tagger', 'stanford-pos/stanford-postagger.jar')

	self.mp  = MusicControl('iml.xml', '/run/media/vidur/Kachra/Music/')
	#self.tc  = TrainControl()
	self.hc  = HardwareControl()
	#self.qc  = QuestionControl()
	#self.ac  = AlarmControl()
	#self.gc  = GreetingControl()
	self.tyc = TypeClassifier(ft_dir[0], ft_dir[1])#"fastText/voiceai.bin")

	def process_message(self, msg):
		msg_words = nltk.word_tokenize(msg)
		original_msg = msg
		#MESSAGE TYPE CLASSIFIERS:
		#1 - Music
		#2 - Brightness and Volume
		#3 - Questions/Google/Wiki
		#4 - Alarm
		#0 - Train POS and NER

		if msg_words[0] == 'xadd' or msg_words[0] == 'xtrain':
			#START TRAINING/ADDING
			return "Train / Add done!"


		textType = self.tyc.classifyText(msg)
		if textType > -1:
			msg=str(textType)
		else:
			return "I'm sorry I didn't get that, Vidur"

		#CATCH POS
		Nouns = []
		Verbs = []
		Adjs  = []
		Numbers = []
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
					else:
						if tup[1] == 'NUM':
							Numbers.append((i, tup[0]))

		saveF = open("allTexts.tsv", 'a')
		saveF.write(msg)
		saveF.write('\n')
		saveF.close()
		
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
			if pos_tagged[0][1] == 'MON':
				Money.append(" ".join([x[0] for x in pos_tagged]))

		#SELECT TYPE CONTROL
		
		if textType == 1:
			#TYPE MUSIC
			#Keywords - play, stop, pause, resume, shuffle - VERBS, music, song(s), track(s), artist, singer, musician, album, band - NOUNS, next, previous - ADJS, ART, PER - ENT	
			KeyVerbs = ['play', 'stop', 'pause', 'resume']
			KeyNouns = ['music', 'song', 'album', 'artist']
			KeyModif = ['next', 'previous']

			MainVerb = ""
			for eachVerb in Verbs:
				verbSub = eachVerb[1].lower()
				found = False
				for eachKey in KeyVerbs:
					if verbSub == eachKey:
						MainVerb = eachKey
						found = True
						break
				if found:
					break

			if MainVerb == 'stop':
				self.mp.Stop()
				return msg

			if MainVerb == 'pause':
				self.mp.Pause()
				return msg

			if MainVerb == 'resume':
				msg = "\n".join([msg, "Playing song :", self.mp.Play()])
				return msg

			Modifier = ""
			for eachAdj in Adjs:
				adjSub = eachAdj[1].lower()
				found = False
				for eachKey in KeyModif:
					if adjSub == eachKey:
						Modifier = eachKey
						found = True
						break
				if found:
					break

			if Modifier == 'next':
				self.mp.Next()
				return msg

			if Modifier == 'previous' or Modifier == 'last':
				self.mp.Prev()
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

			if MainVerb == 'play':
				msg = "\n".join([msg, "Playing song :", self.mp.Play(song_name, artist_name, album_name)])
				#bot.send_text_message(recipient_id, msg)

			return msg
		
		if textType == 2:
			KeyVerbs = ['set', 'increase', 'decrease']
			KeyNouns = ['brightness', 'volume']
			MainVerb = ""
			MainNoun = ""

			for eachVerb in Verbs:
				verbSub = eachVerb[1].lower()
				found = False
				for eachKey in KeyVerbs:
					if verbSub == eachKey:
						MainVerb = eachKey
						found = True
						break
				if found:
					break

			if MainVerb == "":
				return "".join([msg, "\nSorry Vidur, I didn't get that"])

			for eachNoun in Nouns:
				nounSub = eachNoun[1].lower()
				found = False
				for eachKey in KeyNouns:
					if nounSub == eachKey:
						MainNoun = eachKey
						found = True
						break
				if found:
					break

			if MainNoun == "":
				return "".join([msg, "\nSorry Vidur, I didn't get that"])

			percent = -10
			if len(Numbers) > 0:
				percent = int(Numbers[0][1])

			if MainVerb == 'set':
				if percent == -10:
					return "".join([msg, "\nSorry Vidur, I didn't get that"])

				if MainNoun == 'brightness':
					return "".join([msg, self.hc.setBrightness(percent)])

				if MainNoun == 'volume':
					return "".join([msg, self.hc.setVolume(percent)])

			if percent < 0:
				percent = 13

			if MainVerb == 'increase':
				if MainNoun == 'brightness':
					return "".join([msg, self.hc.increaseBrightness(percent)])

				if MainNoun == 'volume':
					return "".join([msg, self.hc.increaseVolume(percent)])

			if MainVerb == 'decrease':
				if MainNoun == 'brightness':
					return "".join([msg, self.hc.increaseBrightness(percent, False)])

				if MainNoun == 'volume':
					return "".join([msg, self.hc.increaseVolume(percent, False)])


			return msg

		return msg

