#!/bin/bash

./fasttext supervised -lr 1.5 -input voiceai-train.tsv -output voiceai
./fasttext test voiceai.bin voiceai-train.tsv
