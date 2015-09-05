#!/usr/bin/env python3

import pywikibot
import re
import difflib
from common import *
from colorama import Fore, Back, Style
import traceback


######################## CONFIG ##############################
EDITOR = 'subl -w'
#############################################################

site = pywikibot.Site('en', 'clubpenguinwiki')
cat = pywikibot.Category(site, 'Category:Furniture & Igloo Catalog')
pages = cat.articlesList()


verbose = True

for page in pages:
	text = page.text

	if verbose: print(page.title())

	text = re.sub(r'^<div class="toccolours mw-collapsible mw-collapsed">\n<center><big>(?:\'\'\')?(.+?)(?:\'\'\')?</big></center>\n<div class="mw-collapsible-content">', r'=== \1 ===', text, flags=re.M)
	text = re.sub(r'^</gallery>\n</div>\n</div>', r'</gallery>', text, flags=re.M)
	text = re.sub(r'^=== (Colors|Flags) ===\n<gallery>', r'=== \1 ===\n<gallery widths="60" heights="60">', text, flags=re.M)
	text = re.sub(r'--(&gt;|>)', r'→', text, flags=re.M)
	text = re.sub(r'\* ?(?:<span class="plainlinks">)?\[http://archives\.clubpenguinwiki\.info/static/images/archives/[^/]+/[^/]+/(.+?\.swf) (.+)](?:</span>)?', r'* [[archives:Media:\1|\2]]', text, flags=re.M)
	text = re.sub(r'^=== (.+?)\'\'\' ===', r'=== \1 ===', text, flags=re.M)
	text = formatting(text)

	if text.find('REDIRECT') > -1:
		print(Style.BRIGHT + pageName + Style.RESET_ALL, 'was redirected.')
		# print(text)
		print()
	else:
		if page.text == text:
			if verbose: print('No change in page ' + page.title() + '. Skipping!')
			continue

		while True:
			d = difflib.Differ()
			diff = d.compare(page.text.splitlines(), text.splitlines())
			diff = map(colorizeDiff, diff)
			print('\n'.join(diff))

			choice = input('Apply [yeN]:').lower()
			if choice == 'e' or choice == '*':
				status, text = edit(EDITOR, text)
				if verbose: print('Updated text; status=', status)
			elif choice == 'y' or choice == '+':
				page.text = text
				page.save('new catalogue layout')
				if verbose: print('\n\n\n')
				break
			else:
				if verbose: print('Skipping', page.title())
				break
