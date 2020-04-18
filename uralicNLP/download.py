import argparse
from . import semfi
from . import uralicApi

def download_semfi(langs):
	for lang in langs:
		semfi.download(lang)

def download(langs):
	for lang in langs:
		uralicApi.download(lang)

if __name__== "__main__":
	parser = argparse.ArgumentParser(description='UralicNLP download languages')
	parser.add_argument('-l','--languages', nargs='+', help='<Required> Languages to download', required=True)
	parser.add_argument("--semfi", action='store_true', help="Download semfi/semur for the specified languages")
	args = parser.parse_args()
	if args.semfi:
		download_semfi(args.languages)
	else:
		download(args.languages)

