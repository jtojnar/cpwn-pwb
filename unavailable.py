#!/usr/bin/env python3

import pywikibot
import re
import difflib
from common import *

######################## CONFIG ##############################
pages = ["The Starlight", "Springtime Sass", "The Shock Top", "Pixelhopper Shirt", "The Huntress", "The Graceful", "The Fiery Flair", "The Silver Sweep", "Mint Beach Dress", "The Gretel", "Coral Beach Dress", "The Do-Re-Mi", "The Wistful", "The Firecracker", "The Riot", "The Flame", "Rap Battler", "Lime Lyricist", "White Pixel Puffle Tee", "Green Pixel Puffle Tee", "Purple Pixel Puffle Tee", "Pink Pixel Puffle Tee", "Gold Pixel Puffle Tee", "Red Pixel Puffle Tee", "Black Pixel Puffle Tee", "Yellow Pixel Puffle Tee", "Brown Pixel Puffle Tee", "Orange Pixel Puffle Tee", "The Country Gal", "Green Slouch Purse", "Golden Bangles", "Bangles", "Redhead Headphones", "The Sunny Side", "Brown Flip Flops", "Grey B-Boy Sneakers", "The Bob 3000", "The Spike 3000", "Puffle Wrangler Hat", "Galactic Space Suit", "Puffle Wrangler Outfit", "Cowboy Boots", "Ring Master Hat", "Ring Master Outfit", "Popcorn (item)", "Untied Sneakers", "The Ringlets", "Beach Dress", "Pink and White Sandals", "Caramel Apple Costume", "Green MP3000", "The Aquamarine", "Tropical Mermaid Costume", "Swashbuckler's Hat", "High Seas Coat", "High Seas Boots", "Treasure Maps", "Telescope", "Green Dance Sweats", "Striped Pirate Bandanna", "Swashbuckler's Coat", "Raggedy Rags", "The Black Widow", "Black Widow Bodysuit", "The Hawkeye", "Hawkeye-wear", "Hawkeye Bodysuit", "Hawkeye Quiver & Bow", "Thor Helmet", "Thor Armor", "Mjolnir", "Captain America Cowl", "Captain America Bodysuit", "Captain America Shield", "THE HULK SMASH", "HULK BODYSUIT", "Nick Fury Eyepatch", "Nick Fury Coat", "Mark 42 Helmet", "Mark 42 Armor", "War Machine Helmet", "War Machine Armor"]
EDITOR = 'subl -w'

#############################################################


site = pywikibot.Site('en', 'clubpenguinwiki')

for pageName in pages:
	page = pywikibot.Page(site, pageName)
	text = page.text
	if text.find('REDIRECT') == -1:
		text = re.sub(r'^(==+)([^= ].+)\1 *$', r'\1 \2 \1', text, flags=re.M)
		text = re.sub(r'border="1" class="wikitable"', r'class="wikitable"', text, flags=re.M)
		text = re.sub(r"^(!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)'''(?:(!!)'''(.+?)''')?)?)?)?)?", r'\1\2\3\4\5\6\7\8\9\10\11\12', text, flags=re.M)
		text = re.sub(r'^(\|[^=\n]*)(?:([^ ])| )=(?:([^ ])| )', r'\1\2 = \3', text, flags=re.M)
		text = re.sub(r'^(\|(colspan|rowspan)) = ', r'\1=', text, flags=re.M)
		text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/photos/\1\.swf .+ \(photos?\)\]', r'{{Photoswf|\1}}', text)
		text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/paper/\1\.swf .+ \(paper\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/sprites/\1\.swf .+ \(sprites?\)\]', r'{{Itemswf|\1}}', text)
		text = re.sub(r'([^\n])(\n\[\[pt:(?!\]\]).+\]\])', r'\1\n\2', text)
		text = re.sub(r'([^\n])\n(==+)(.+)\2$', r'\1\n\n\2\3\2', text, flags=re.M)
		text = re.sub(r'^\}\}([^\n])', r'}}\n\n\1', text, flags=re.M)
		text = re.sub(r'== SWFs? ==\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/icons/(\d+)\.swf .+ \(icons?\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/paper/\1\.swf .+ \(paper\)\]\n\* ?\[http://media1\.clubpenguin\.com/play/v2/content/global/clothing/sprites/\1\.swf .+ \(sprites?\)\]', r'{{Itemswf|\1}}', text)
		text = re.sub(r'^(\{\{(?:Itemswf|Photoswf|Furnitureswf)\|[^}\n]+\}\}\n)([^\n])', r'\1\n\2', text, flags=re.M)
		text = re.sub(r'^([#:*]+)([^ ])', r'\1 \2', text, flags=re.M)

		text = re.sub(r'^(\|available = )Yes', r'\1No', text, flags=re.M)
		text = re.sub(r'are able to (buy|purchase|obtain|get)', r'were able to \1', text)
		text = re.sub(r'can (buy|purchase|obtain|get)', r'could \1', text)
		text = re.sub(r'\{\{Available\|Items}}\n\|\|', r'{{Available|Items}}||', text)
		text = re.sub(r'\{\{Available\|Items}}', r'June 30, 2015', text)
		text = re.sub(r'\{\|class="wikitable" ', r'{|class="wikitable"', text)

		if page.text == text:
			print('No change in page ' + pageName + '. Skipping!')
			continue

		while True:
			d = difflib.Differ()
			diff = d.compare(page.text.splitlines(), text.splitlines())
			diff = map(colorizeDiff, diff)
			print('\n'.join(diff))

			choice = input('Apply [yeN]:').lower()
			if choice == 'e':
				status, text = edit(EDITOR, text)
				print('Updated text; status=', status)
			elif choice == 'y':
				page.text = text
				page.save('unavailable')
				print('')
				print('')
				print('')
				break
			else:
				print('Skipping', pageName)
				break
	else:
		print(pageName, 'was redirected:')
		print(text)
		print()
