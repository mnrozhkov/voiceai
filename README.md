# VOICEAI
Voiceai is a library for controlling a machine using text and voice based interface. It uses

1. The [Stanford NER tagger](http://nlp.stanford.edu/software/CRF-NER.shtml) for NER Tagging
2. The [Stanford POS tagger](http://nlp.stanford.edu/software/tagger.shtml) for POS Tagging
3. The Facebook [fastText](https://github.com/facebookresearch/fastText) api for text classification
4. The [CMU Sphinx](https://cmusphinx.sourceforge.net) api for voice recognition(**not added yet**)
5. The [pyItunes](https://github.com/liamks/pyitunes) api for parsing iTunes XML for music data
6. The [pint](https://github.com/hgrecco/pint) library for cross units and dimensions conversion

## Features 
The following features are available : 

1. Music control
  1. Play Song/Artist/Album
  2. Pause
  3. Stop
  4. Resume
  
2. Hardware Control
  1. Adjust volume
  2. Adjust brightness
  
3. Training Control
  1. Added new sentences and tokens for learning
  2. Train POS, NER, FastText with for better accuracy and language
  
4. Conversion Control
  1. Convert units and dimensions
  2. Convert currencies (*internet required*) ([fixer.io](http://api.fixer.io/))
  
5. Web search Control
  1. Search anything using the [DuckDuckGo](https://duckduckgo.com) api

6. Greeting Control
  1. Engage in a casual conversation with the bot

7. Alarm Control
  1. Set alarms and reminders


### Installation
Place the voiceai directory in your project

```
git clone https://github.com/vidursatija/voiceai.git
```

### Usage

```python
import voiceai
print(voiceai.process_message("Play some Taylor Swift songs")) #Music control
print(voiceai.process_message("Increase brightness by 10%")) #Hardware control
print(voiceai.process_message("How many miles are there in a kilometer?")) #Conversion control
print(voiceai.process_message("Search the web for latest news")) #Net control
print(voiceai.process_message("xtrain-pos")) #Train control
```
