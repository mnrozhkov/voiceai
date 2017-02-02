#!/bin/bash

java -Xmx1792m -Xms512m -cp stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -props voiceai-pos.tagger.props
