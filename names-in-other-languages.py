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
cat = pywikibot.Category(site, 'Category:Missing name in other language')
pages = cat.articlesList()


def getGoodLabel(i):
	if 'prompt' in i and i['prompt'].find('##') == -1 and i['prompt'].strip() != '':
		if 'label' in i and i['label'].find('##') == -1 and i['label'].strip() != '' and i['prompt'] != i['label']:
			print(Fore.MAGENTA + 'Imparity:', i['prompt'].strip(), '≠', i['label'].strip(), Style.RESET_ALL)
		return i['prompt'].strip()
	elif 'label' in i and i['label'].find('##') == -1 and i['label'].strip() != '':
		return i['label'].strip()
	else:
		return '{{Untranslated}}'

def getGoodName(i):
	if i['name'].find('##') == -1 and i['name'].strip() != '':
		return i['name'].strip()
	else:
		return '{{Untranslated}}'

def getItemLabels(fileName, idKey):
	ret = {}
	for l in langs:
		ret[l] = {int(i[idKey]): getGoodLabel(i) for i in getDataFile(l, fileName)}
	return ret


def getIglooLabels(fileName):
	ret = {}
	for l in langs:
		ret[l] = {int(k): getGoodName(i) for k, i in getDataFile(l, fileName).items()}
	return ret

def getStampLabels(fileName, idKey):
	ret = {}
	for l in langs:
		stamps = sum([i['stamps'] for i in getDataFile(l, fileName)], [])
		ret[l] = {int(s[idKey]): getGoodName(s) for s in stamps}
	return ret


items = furniture = stamps = igloos = flooring = locations = pitems = None
for page in pages:
	text = page.text
	cats = [cat.title() for cat in page.categories()]

	print(page.title(), cats)

	if 'Category:Puffle Food' in cats or 'Category:Puffle Toys' in cats or 'Category:Puffle Items' in cats or 'Category:Puffle Hats' in cats:
		if not pitems:
			pitems = getItemLabels('puffle_items.json', 'puffle_item_id')
		cur = pitems
	elif 'Category:Furniture' in cats:
		if not furniture:
			furniture = getItemLabels('furniture_items.json', 'furniture_item_id')
		cur = furniture
	elif 'Category:Flooring' in cats:
		if not flooring:
			flooring = getItemLabels('igloo_floors.json', 'igloo_floor_id')
		cur = flooring
	elif 'Category:Igloo Locations' in cats:
		if not locations:
			locations = getItemLabels('igloo_locations.json', 'igloo_location_id')
		cur = locations
	elif 'Category:Igloos' in cats:
		if not igloos:
			igloos = getIglooLabels('igloos.json')
		cur = igloos
	elif 'Category:Stamps' in cats:
		if not stamps:
			stamps = getStampLabels('stamps.json', 'stamp_id')
		cur = stamps
	elif 'Category:Items' in cats:
		if not items:
			items = getItemLabels('paper_items.json', 'paper_item_id')
		cur = items
	else:
		print('Category invalid', page.full_url())
		continue

	try:
		itemId = int(re.search(r'\|' + ('stamp' if cur == stamps else '') + 'id ?= ?(\d+)', text).group(1))
		text = re.sub(r'\{\{OtherLanguage(?!\}\}).+?\}\}', r'''{{OtherLanguage
|portuguese = ''' + cur['pt'][itemId] + '''
|french = ''' + cur['fr'][itemId] + '''
|spanish = ''' + cur['es'][itemId] + '''
|german = ''' + cur['de'][itemId] + '''
|russian = ''' + cur['ru'][itemId] + '''
}}''', text, flags=re.M | re.S)
	except Exception as e:
		print(Back.RED + Fore.WHITE + traceback.format_exc() + Style.RESET_ALL)
		continue


	if text.find('REDIRECT') == -1:
		if page.text == text:
			print('No change in page ' + page.title() + '. Skipping!')
			continue

		while True:
			d = difflib.Differ()
			diff = d.compare(page.text.splitlines(), text.splitlines())
			diff = map(colorizeDiff, diff)
			print('\n'.join(diff))

			print(Fore.YELLOW, end='')
			dirty = False
			for l in langs:
				translated = re.search(r'\|' + fullLangs[l] + ' ?= ?([^\n|]+)', page.text)
				if not translated:
					print(Fore.BLUE + l, Fore.YELLOW)
				elif translated.group(1).strip() != cur[l][itemId] and cur[l][itemId] != '{{Untranslated}}':
					print(l, end=' ')
					dirty = True
			print(Style.RESET_ALL)

			if dirty:
				choice = 'n'
			else:
				choice = 'y'

			# choice = input('Apply [yeN]:').lower()
			if choice == 'e' or choice == '*':
				status, text = edit(EDITOR, text)
				print('Updated text; status=', status)
			elif choice == 'y' or choice == '+':
				page.text = text
				page.save('names in other languages')
				print('')
				print('')
				print('')
				break
			else:
				print('Skipping', page.title())
				break
	else:
		print(page.title(), 'was redirected:')
		print(text)
		print()
