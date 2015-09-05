#!/usr/bin/env python3

import pywikibot
import re
import difflib
from common import *

######################## CONFIG ##############################
pages = ["The Up Sweep", "The County Fair", "Toasty Cocoa", "Orange Balloon", "Mixed Bracelets", "Teal Tee", "Green Tee", "Pink Tee", "The Right Direction", "Navy Royale Tux", "The Willow Wisp", "Shimmer Diva Dress", "Gold Chandelier Earrings", "Charm Bangle", "The Sea Breeze", "Plaid Hoodie Outfit", "Lemon Button Blouse", "The Glamorous", "Midnight Glamor Dress", "Jet Pack", "The Right Stuff", "Prom King Tux", "Compact", "Makeup Palette", "Thin Mustache", "Lashful Eyes", "Jellyfish Necklace", "Priceless Necklace", "Beach Chain", "Spy Visor", "Daisy Glasses", "Orange Tie", "Spiky Dubstep Purse", "Strawberry Cake Purse", "Card-Jitsu Carryall", "Blue Dragon Costume", "Purple Butterfly Wings", "Raven Wings", "Lion Costume", "Merguin Fin", "Blue Mermaid Costume", "The Cerulean Lagoon", "Puffle Mania Shirt", "Puffle Hoodie", "Pufflescape Ball", "Puffle Pirate Dress", "Starship Suit", "Planet Zeta Costume", "The Squid Lid", "The Drama", "Boho Style Outfit", "Pink Ice Cream", "Gold Sparkle Loafers", "The Flipster", "Surf 'n Style Outfit", "Green High Tops", "Red Letterman Jacket", "Water Bottle (clothing)", "Purple Sneakers", "Brown Striped Fedora", "Gold Letterman Jacket", "The Side Swirl", "Polka-Dot Bandanna", "The Vintage", "Laptop", "Aqua Bead Necklace", "Seafoam Slip Ons", "Flower Basket", "Cream Sandals", "The Striking", "Tags", "Black Shoulder Bag", "The Chilled", "Tourist Camera", "Trek Boots", "Starshine Makeup", "Interstellar Makeup", "Metropolis Makeup", "Utopia Makeup", "Royal Eyelashes", "Icy Eyelashes", "Fancy Lashes", "Winged Eyeliner", "Camera", "Video Camera (ID 5054)", "Black Toque", "Press Cap", "Caveguin Helmet", "Cop Cap", "Police Helmet", "Driver's Cap", "Purple Toque", "The Styled Messy", "Cat Burglar Mask", "Police Aviators", "Pixel Shades", "Mask", "Nautical Necklace", "Elf Suit", "City's Finest Uniform", "Up To No Good Suit", "Ghost Catcher Uniform", "Furry Shorts", "Goes with Everything Shirt", "Popcorn_(item)", "Yellow Monster Wings", "Trusty Spear", "Break a Leg Cast", "Blue Skater Shoes", "Hard Hat", "Green Ball Cap", "Pink Ball Cap", "Pilgrim Hat", "Top Hat", "Chef Hat", "Jester Hat", "Blue Earmuffs", "Red Ball Cap", "Blue Ball Cap", "Admirals Hat", "Bonnet", "Divers Helmet", "Gold Viking Helmet", "Snowboard Helmet", "Firefighter Hat", "Clown Hair", "Bird Mascot Head", "Stocking Cap", "Woodsman's Hat", "Cocoa Bunny Ears", "The Rocker", "The Spikester", "The Disco", "The Flutterby", "The Sunstriker", "The Surf Knot", "Pink Visor", "The Firestriker", "Frankenpenguin Hat", "Faery Hair", "Snowman Head", "The Freestyle", "The Shamrocker", "Swim Cap and Goggles", "The Befluttered", "The Starlette", "The Sidewinder", "Ring Master Hat", "White Head Band", "Baseball Helmet", "The Posh", "Outback Hat", "The Flow", "The Sunray", "The Shock Wave", "Dazzling Blue Top Hat", "The Tousled", "The Vibrant", "Cumberband Hat", "The Prep", "The Chill Out", "Snow Fairy Hair", "Blizzard Wizard Hat", "Ogre Ears", "Yellow Toque", "The Sidekick", "Reindeer Head", "The Vintage", "Brown Teal Cap", "The Frost", "The Brunette", "The Elegant", "The Scarlet Star", "The Short & Sweet", "The Part", "Red Mohawk", "Puffle Cap", "Green Hard Hat", "Brown Striped Fedora", "Green Cap", "White Cocoa Bunny Ears", "The Band", "The Trend", "The Bonny Curls", "First Mate's Hat", "Striped Pirate Bandanna", "Swashbuckler's Hat", "Commander's Hat", "The Razzmatazz", "The Aquamarine", "The Adventurer", "The Sunburst", "The Flip", "The Golden Waves", "Yellow Climbing Helmet", "Red Climbing Helmet", "The Summer Tussle", "Jam Cap", "The Sun Rays", "Cleo Headdress", "The Side Swept", "The Skater", "The Chic", "Elf Pigtails", "Blue Goggles", "3D Glasses", "Designer Glasses", "White Diva Sunglasses", "Aviator Sunglasses", "Curly Mustache", "Humbug Spectacles", "Green Snorkel", "Pink Snorkel", "Ski Goggles", "Green Face Paint", "Yellow Face Paint", "Adventure Face Paint", "Red Face Paint", "Blue Face Paint", "Castaway Face Paint", "Gray Beard", "Santa Beard", "Pink Diva Shades", "Sleet Stopper", "Snow Stopper", "Slush Stopper", "Blue Aviator Shades", "Blue Starglasses", "Indigo Sunglasses", "Golden Shades", "Pink Starglasses", "Mask of Justice", "Fiendish Mask", "Valiant Mask", "Sinister Mask", "Giant White Sunglasses", "Watermelon Tiki Paint", "Apple Tiki Paint", "Grape Tiki Paint", "Pineapple Tiki Paint", "Spectacles", "The Mystery", "The Golden Secret", "The Phantom", "Butler Brow", "Old Maid Makeup", "Mystic Makeup", "Majestic Makeup", "Prehistoric Tusks", "Caveguin Face Paint", "Biggest Brow", "Grillz", "2 Cool Glasses", "Blue Scarf", "Snare Drum", "Pendant Necklace", "Ruffle Collar", "Seeing Spots Scarf", "Messenger Bag", "Cheesy Necktie", "Mullet Necktie", "Smiley Necktie", "Jade Necklace", "Vinyl Messenger Bag", "McKenzie's Necklace", "Pink Designer Scarf", "Green Trendy Scarf", "Blue Striped Scarf (ID 3012)", "Compass", "Flower Messenger Bag", "Flame Messenger Bag", "Blue Striped Scarf (ID 3035)", "Smitten Scarf", "Checkered Tote", "Green Cotton Scarf", "Gold Chain", "Conga Drums", "Surf Necklace", "All Access Pass (ID 3050)", "Blue Climbing Rope", "Yellow Climbing Rope", "Purple Rugby Scarf", "Popcorn Tray", "Blue Patched Bag", "Polka-Dot Bandanna", "Royal Blue Robe", "Raindrop Necklace", "Pink Zebra Scarf", "Bumblebee Scarf", "Noteworthy Necklace", "Silver Star Necklace", "Blue Accordion", "Tundra Board", "Electric Pink Snowboard", "Blast-Off Board", "Abracadabra Cape", "Magician's Cloak", "Pegasus Wings", "Feather Necklace", "Supreme Toy Sack", "Bronze Music Note Necklace", "Blue Scuba Tank", "Aqua Bead Necklace", "Cornflower Scarf", "Purple Beaded Necklace", "Golden Wings", "Video Camera (ID 3121)", "Pauldrons of Justice", "Fiendish Pauldrons", "Toothy Necklace", "Kukui Nut Necklace", "Clam Shell Collar", "Sea Foam Pearls", "Leather Satchel", "Puffle Care Sash", "Gold Charm Necklace", "Sleigh Bells", "Thick Hide Cloak", "Prehistoric Necklace", "Great Bone Cloak", "Stone Bow Tie", "Lavender Knit Scarf", "Tags", "Daisy Chain", "14K Fish Necklace", "Hawaiian Shirt", "Wetsuit", "Clown Suit", "Jean Jacket", "Ballerina", "Long Johns", "Leprechaun Tuxedo", "Red Letterman Jacket", "Lifeguard Shirt", "Firefighter Jacket", "Safety Vest", "Ski Patrol Jacket", "Red Baseball Uniform", "Blue Baseball Uniform", "Sport Bikini", "Sarong", "Divers Suit", "Orange Rocker Shirt", "Black Cowboy Shirt", "Pink Cowgirl Shirt", "Green Vest", "Purple Figure Skating Dress", "Snowman Body", "Gingerbread Costume", "Yellow Winter Jacket", "Spikester Threads", "Freestyle Threads", "Racing Swimsuit", "Mountain Climber Gear", "Swashbuckler Outfit", "Blue Tuxedo", "Lavender Gown", "Blue Dazzle Dress", "Black Party Dress", "White Tuxedo", "Amethyst Dress", "Pink Tennis Outfit", "Orange Tennis Outfit", "Purple Wetsuit", "Yellow Summer Outfit", "Orange Hawaiian Outfit", "Blue Star Swimsuit", "Blue Board Shorts", "Black Hawaiian Shorts", "Green Flower Bikini", "Rocker Outfit", "Dazzling Blue Tux", "Electro T-Shirt", "Pink Polka-dot Dress", "Pilot's Jacket", "Girl's Sweater Vest", "Boy's Sweater Vest", "Ring Master Outfit", "Snow Fairy Dress", "Butterfly Dress", "Blizzard Wizard Robe", "Ladybug Suit", "Fuzzy Experiment", "Black Whirlpool Snowsuit", "Reindeer Costume", "Tree Costume", "Cozy Winter Coat", "Puffle Pullover", "Pink Quilted Coat", "Orange Vest", "Summer Threads", "Buttercup Ball Gown", "Petal Pattern Dress", "Ruffle Dress", "Classy T-Shirt", "Admirals Coat", "Green Recycle Shirt", "White Cocoa Bunny Costume", "Rustic Tunic and Skirt", "City Top and Jacket", "Squire Outfit", "Seafarer's Gown", "Pirate Lass", "Swashbuckler's Coat", "Coral Mermaid Costume", "Tropical Mermaid Costume", "Castaway's Clothing", "Floral Bikini", "Yellow Pop Outfit", "Yellow Expedition Jacket", "Blue Expedition Jacket", "Blue Duck", "Waddle On Hoodie", "Magenta Sunset Hoodie", "Yellow Tracksuit", "Puffle Raincoat", "Blue Snow Jacket", "Pink Sled Coat", "Santa Suit", "Life Jacket (ID 4292)", "Checked Crop Coat", "Gold Wristwatch", "Silver Watch", "Pot O'Gold", "Black Electric Guitar", "Snow Shovel", "Violin", "Silver Surfboard", "Flame Surfboard", "Daisy Surfboard", "Tennis Racket", "Crystal Staff", "Spikester Cuffs", "Green Shield", "Orange Shield", "Purple Shield", "Acoustic Sunburst Guitar", "Pink Electric Guitar", "Microphone", "Mixed Bracelets", "Denim Purse", "Bracers", "Binoculars", "Blue Puffle Stuffie", "Smitten Mittens", "Teal Bracelet", "Black MP3000", "Floral Clutch Bag", "Brown Leather Cuffs", "Water Bottle", "Pirate Arm Bands", "Foraged Bracelet", "Leather Watch", "Garden Shovel", "First Aid Kit", "Cosmic Umbrella", "Polka Dot Umbrella", "Candy Cane Wing-warmers", "Paddle", "Pink MP3000", "Gold Shield", "Stompin Bob Cuff", "Green and Blue Maracas", "Oil Slick Guitar", "Telescope", "Treasure Maps", "Bangles", "Bunch of Balloons", "Dumbbells", "Ghoul Detector 3000", "Ghostly Gallop", "Fire Blossom Fan", "Water Lotus Fan", "Sushi Tray", "Candy Cane Cane", "Green MP3000", "Pearl Clutch Bag", "Fireworks Bangle", "Thunder Blade", "Acid Guitar!", "Sweet Spikester Cuffs", "Freezing Super Gloves", "Shocking Super Gloves", "Cosmic Super Gloves", "Grape Spear", "Kiwi Purse", "Lime Laptop", "Antique Mirror", "Pocket Watch", "Masquerade Fan", "Mint Purse", "Rugged Radio", "Green Chic Purse", "Brown Shoes", "Black Sneakers", "Ballet Shoes", "Blue Sneakers", "Running Shoes", "Yellow Sandals", "Winter Boots", "Bunny Slippers", "Cowboy Boots", "Elf Shoes", "Yellow Rubber Boots", "Pink Sandals", "Brown Sandals", "Blue Rollerskates", "Pink Rollerskates", "Wool Socks", "Fuzzy Boots", "Pink Flippers", "Blue Flower Sandals", "White Dress Shoes", "Tennis Shoes", "Plated Shoes", "Pointy Shoes", "Green Hiking Boots", "Burgundy Buckle Shoes", "Ladybug Shoes", "Vintage Boots", "Untied Sneakers", "Pink Canvas Shoes", "Gray Boots", "Nautical Boots", "Commander's Boots", "Yellow Hiking Shoes", "Red Hiking Shoes", "Clown Shoes", "Blue Striped Rubber Boots", "Snowboard Boots", "Lumberjack Boots", "Blue Canvas Shoes", "Astro Boots", "Peak Boots", "Rooster Feet", "Stompin' Boots", "Orange Frankenfeet", "Seismic Sandals", "Brown Snow Bunny Boots", "Magenta Sandals", "Sparkly Sea Foam Slippers", "Awards Background", "Aqua Disco Background", "Fashion Show background", "Walk of Fame background", "Red and Purple Plaid background", "Patio View Background", "Rainy Day background (2012 version)", "Bamboo Grove background"]
EDITOR = 'subl -w'
available = True
releaseDate = 'August 5, 2015'
previousReleaseDates = ['June 30, 2015']
#############################################################


site = pywikibot.Site('en', 'clubpenguinwiki')

for pageName in pages:
	page = pywikibot.Page(site, pageName)
	text = page.text
	if text.find('REDIRECT') > -1:
		print(Style.BRIGHT + pageName + Style.RESET_ALL, 'was redirected.')
		# print(text)
		print()
	elif text.find(releaseDate) > -1 or all([text.find(d) > -1 for d in previousReleaseDates]):
		print(Style.BRIGHT + pageName + Style.RESET_ALL, 'was skipped as already updated.')
	else:
		text = formatting(text)

		if not available:
			text = re.sub(r'^(\|available = )Yes', r'\1No', text, flags=re.M)
			text = re.sub(r'are able to (buy|purchase|obtain|get)', r'were able to \1', text)
			text = re.sub(r'can (buy|purchase|obtain|get)', r'could \1', text)
			text = re.sub(r'\{\{Available\|Items}}\n\|\|', r'{{Available|Items}}||', text)
			text = re.sub(r'\{\{Available\|Items}}', releaseDate, text)
			text = re.sub(r'\{\|class="wikitable" ', r'{|class="wikitable"', text)
		else:
			text = re.sub(r'^(\|available = )No', r'\1Yes', text, flags=re.M)
			text = re.sub(r'were able to (buy|purchase|obtain)', r'are able to \1', text)
			text = re.sub(r'could (buy|purchase|obtain)', r'can; \1', text)
			text = re.sub(r'^\|(?:rowspan="?(\d+)"?\|)?(Penguin Style\|\|)', (lambda m: '|rowspan=' + str(int(m.group(1) if m.group(1) else 1) + 1) + '|' + m.group(2)), text, flags=re.M)
			text = re.sub(r'\n\|}', '\n|-\n|' + releaseDate + '||{{Available|Items}}\n|}', text)


		if page.text == text:
			print(Style.BRIGHT + pageName + Style.RESET_ALL + ' was skipped as unchanged.')
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
				page.save('available' if available else 'unavailable')
				print('')
				print('')
				print('')
				break
			else:
				print('Skipping', Style.BRIGHT + pageName + Style.RESET_ALL)
				break
