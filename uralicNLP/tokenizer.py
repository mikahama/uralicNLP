import re
import mikatools

sentence_end = set("!?。……‥！？。⋯…؟჻!…")
numbers = set("0123456789١٢٣٤٥٦٧٨٩٠")

abrvs = mikatools.json_load(mikatools.script_path("abrvs.json"))
abrv_regex = re.compile(r"(^|\s)(" + "|".join([re.escape(a) for a in abrvs]) + ")$")

def _ends_in_abrv(text):
	return abrv_regex.search(text.lower()) is not None

def sentences(text):
	parts = []
	current_s = ""
	previous_break = False
	for i, c in enumerate(text):
		if c in sentence_end:
			#End of a sentence, not a dot
			if len(current_s) > 0:
				#There is a current sentence, apped it and clear it
				parts.append(current_s + c)
				current_s = ""
			elif len(parts) > 0:
				#No current sentence, add to a previous sentence
				parts[len(parts)-1] += c
			else:
				#Make it a current sentence
				current_s = c
		elif c == ".":
			#A dot
			if len(current_s) == 0:
				#no current sentence
				if len(parts) > 0:
					#append
					parts[len(parts)-1] += c
				else:
					current_s = c
			elif len(current_s) > 0 and current_s[-1] in numbers:
				#previous is a number
				current_s += c
			elif _ends_in_abrv(current_s):
				#abreviation
				current_s += c
			elif len(text) > i+1 and len(text[i+1].strip()) != 0:
				#dot is not followed by a space
				current_s += c
			else:
				#dot ending a sentence
				parts.append(current_s + c)
				current_s = ""
		elif c == "\n":
			#line break
			if previous_break and len(current_s) > 0:
				parts.append(current_s)
				current_s = ""
			if not previous_break and len(current_s) > 0:
				current_s += c
			previous_break = True
			continue
		elif c == "\r":
			#Windows line break
			continue
		else:
			#Any other character
			current_s += c
		previous_break = False
	if len(current_s) > 0:
		parts.append(current_s)
	space_regex = re.compile(r"\s+")
	parts = [space_regex.sub(" ", part).strip() for part in parts]
	parts = [part for part in parts if len(part) > 0]
	return parts




def words(text):
	pass

def tokenize(text):
	pass