from colorama import Fore, Back, Style
import urllib.request
import os, tempfile
import json
import re

def formatting(text):
	text = re.sub(r'^(==+)([^= ].+)\1 *$', r'\1 \2 \1', text, flags=re.M)
	text = re.sub(r'border="1" class="wikitable"', r'class="wikitable"', text, flags=re.M)
	text = re.sub(r"^(!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)''')?)?)?)?)?", r'\1\2\3\4\5\6\7\8\9\10\11\12', text, flags=re.M)
	text = re.sub(r'^(\|[^=\n]*)(?:([^ ])| )=(?:([^ ])| )', r'\1\2 = \3', text, flags=re.M)
	text = re.sub(r'^(\|(colspan|rowspan)) = ', r'\1=', text, flags=re.M)
	text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/photos/\1\.swf .+ \(photos?\)\]', r'{{Photoswf|\1}}', text)
	text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/paper/\1\.swf .+ \(paper\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/sprites/\1\.swf .+ \(sprites?\)\]', r'{{Itemswf|\1}}', text)
	text = re.sub(r'([^\n])(\n\[\[pt:(?!\]\]).+\]\])', r'\1\n\2', text)
	text = re.sub(r'([^\n=])\n(==+)(.+)\2$', r'\1\n\n\2\3\2', text, flags=re.M)
	text = re.sub(r'^\}\}([^\n])', r'}}\n\n\1', text, flags=re.M)
	text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/paper/\1\.swf .+ \(paper\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/sprites/\1\.swf .+ \(sprites?\)\]', r'{{Itemswf|\1}}', text)
	text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/sprites/\1\.swf .+ \(sprites?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/paper/\1\.swf .+ \(paper\)\]', r'{{Itemswf|\1}}', text)
	text = re.sub(r'^(\{\{(?:Itemswf|Photoswf|Furnitureswf)\|[^}\n]+\}\}\n)([^\n])', r'\1\n\2', text, flags=re.M)
	text = re.sub(r'^([#:*]+)([^ #:*])', r'\1 \2', text, flags=re.M)
	text = re.sub(r'[  ]+$', '', text, flags=re.M)

	return text

def edit(editor, content=''):
	f = tempfile.NamedTemporaryFile(mode='w+')
	if content:
		f.write(content)
		f.flush()
	command = editor + " " + f.name
	status = os.system(command)
	f.seek(0, 0)
	text = f.read()
	f.close()
	assert not os.path.exists(f.name)
	return (status, text)


def colorizeDiff(line):
	if line[0] == '-':
		return Fore.RED + line + Style.RESET_ALL
	elif line[0] == '+':
		return Fore.GREEN + line + Style.RESET_ALL
	elif line[0] == '?':
		return '\033[F\r'
		return Fore.YELLOW + line + Style.RESET_ALL
	else:
		return line

def getDataFile(lang, fileName):
	fname = lang + '_' + fileName
	if os.path.isfile(os.path.abspath(fname)):
		items_file = open(fname)
		return json.loads(items_file.read())
	else:
		items_file = urllib.request.urlopen('http://cdn.clubpenguin.com/play/' + lang + '/web_service/game_configs/' + fileName).read().decode('utf-8')
		with open(fname, 'w') as f:
			f.write(items_file)
		return json.loads(items_file)

langs = ['pt', 'fr', 'es', 'de', 'ru']
fullLangs = {'pt': 'portuguese', 'fr': 'french', 'es': 'spanish', 'de': 'german', 'ru': 'russian'}
