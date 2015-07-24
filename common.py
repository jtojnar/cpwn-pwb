from colorama import Fore, Back, Style
import urllib
import os, tempfile
import json

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
