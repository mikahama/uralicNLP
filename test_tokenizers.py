from uralicNLP import tokenizer
from mikatools import *


#s = "Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't. Государственный гимн Российской Федерации. Государственный гимн Российской Федерации. "

#print(tokenizer.words(s))


s = open_read("test_data/fi_text.txt").read()
for se in tokenizer.tokenize(s):
	print(se)

