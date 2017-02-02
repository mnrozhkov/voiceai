#!/bin/bash

java -mx1g -Xms512m -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop voiceai-ner.prop
