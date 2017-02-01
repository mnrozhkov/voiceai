import os
from subprocess import Popen, PIPE

class TrainControl():

	def __init__(self):
		self.posAddDir = 'newText.tsv'
		self.posOrigDir = 'brownCorp.tsv'
		self.posTrainDir = 'trainpos.tsv'
		self.posModelDir = 'voiceai-pos.tagger'
		self.posPropsDir = 'voiceai-pos.tagger.props'
		self.posTaggerDir = 'stanford-postagger.jar'

		self.nerAddDir = 'extras.tsv'
		self.nerMusicDir = 'musicxml.tsv'
		self.nerModelDir = 'voiceai-ner.ser.gz'
		self.nerPropsDir = 'voiceai-ner.prop'
		self.nerTaggerDir = 'stanford-ner.jar'

		self.ftAddDir = 'voiceai-train.tsv'
		self.ftModelDir = 'voiceai'
		self.ftSupervisedDir = 'fasttext'
	
	def addPOSTagger(self, msg):
		os.chdir('stanford-pos')
		addfile = open(self.posAddDir, 'a')
		addfile.write(msg)
		addfile.write('\n')
		addfile.close()
		os.chdir('..')

	def trainPOSTagger(self):
		os.chdir('stanford-pos')
		trainfile = open(self.posTrainDir, 'w')
		addfile = open(self.posAddDir, 'r')
		brownfile = open(self.posOrigDir, 'r')

		for line in brownfile:
			trainfile.write(line)

		for line in addfile:
			trainfile.write(line)

		trainfile.close()
		addfile.close()
		brownfile.close()
		os.chdir('..')
		#trainProcess = Popen(["java", "-mx1g", "-cp", self.posTaggerDir, "edu.stanford.nlp.tagger.maxent.MaxentTagger", "-props", self.posPropsDir])

	def addNERTagger(self, msg):
		os.chdir('stanford-ner')
		words = msg.split()
		tag = words[-1].upper()
		tokens = words[:-1]

		addfile = open(self.nerAddDir, 'a')
		for token in tokens:
			addfile.write(token)
			addfile.write('\t')
			addfile.write(tag)
			addfile.write('\n')

		addfile.write('\n')
		addfile.close()
		os.chdir('..')

	def trainNERTagger(self):
		os.chdir('stanford-ner')
		trainProcess = Popen(["java", "-mx1g", "-cp", self.nerTaggerDir, "edu.stanford.nlp.ie.crf.CRFClassifier", "-prop", self.nerPropsDir])
		os.chdir('..')
	def addFt(self, msg):
		addfile = open(self.ftAddDir, 'a')
		words = msg.split()
		msg = msg.lower()
		label = words[-1]
		tokens = words[:-1]
		addfile.write("".join(['__label__', label, ' , ']))
		addfile.write(" ".join(tokens))
		addfile.close()

	def trainFt(self):
		trainProcess = Popen([self.ftSupervisedDir, "supervised", "-input", self.ftAddDir, "-output", self.ftModelDir])
