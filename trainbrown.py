cats = open('../nltk_data/corpora/brown/cats.txt', 'r')
fw = open("stanford-pos/brownCorp.tsv", "w")
for line in cats:
	lwords = line.split()
	filename = "".join(['../nltk_data/corpora/brown/', lwords[0]])
	f = open(filename, 'r')
	#fw = open("".join(['brownNER/', lwords[0]]), 'w')
	for l in f:
		l = l.strip()
		if l=='':
			continue

		words = l.split()
		for word in words:
			corp = word.split('/')
			wrd = corp[0]
			tags = corp[1]

			tag = tags[:2]
			wrdtag = ""

			if len(tags) > 4 and tags[-2]=="t" and tags[-1]=="l":
				wrdtag == "ENT"
			else:
				if tag=="np":
					wrdtag = "ENT"
				else:
					if tag=="ab" or tag=="jj" or tag=="ap" or tag == "od":
						wrdtag = "ADJ"
					else:
						if tag=="at" or tag=="dt" or tag=="pn" or tag=="pp" or tag=="pr":
							wrdtag = "PRT"
						else:
							if tag=="be" or tag=="hv" or tag=="md" or tag=="vb" or tag=="do":
								wrdtag = "VER"
							else:
								if tag=="cs" or tag=="cc":
									wrdtag = "CON"
								else:
									if tag=="ex" or tag=="ql" or tag=="rb" or tag=="rn" or tag=="rp":
										wrdtag = "ADV"
									else:
										if tag=="in" or tag=="to":
											wrdtag = "PRE"
										else:
											if tag=="nn" or tag=="nr":
												wrdtag = "NNN"
											else:
												if tag=="uh":
													wrdtag = "ITJ"
												else:
													if tag=="fw":
														wrdtag = "ENT"
													else:
														if tag=="wp" or tag=="wd" or tag=="wq" or tag=="wr":
															wrdtag = 'QUS'
														else:
															if tag == "cd":
																wrdtag = 'NUM'
															else:
																wrdtag = "."
			if wrdtag == "":
				wrdtag = "ENT"
			fw.write(wrd)
			fw.write('_')
			fw.write(wrdtag)
			fw.write(' ')
		fw.write('\n')
cats.close()	
