
import re

def safe_str(s):
	"""Forces a string to be latin, any unknown characters are changed to a ?"""
	try:
		sss = s.decode("ascii")
	except UnicodeDecodeError:
		print "UNI=", s
		safeS = ""
		for cIdx in  range(0, len(s)):
			singleS = s[cIdx]
			if ord(singleS) < 128:
				safeS += singleS
			else:
				safeS += "?"
		sss = safeS
	return sss


def mk_point(lat=None, lon=None, alt=None):
	"""Creates a `POINT()`m or `POINTZ()` if altitude set"""
	if alt != None:
		return "POINTZ(%s %s %s)" %(lon, lat, alt)
	return "POINT(%s %s)" %(lon, lat)


def xsplit(line):
	"""A convenience function for parsing xplane. Unlike python `str.split()`, this splits the line by space and removes blanks
		eg `  01   56.7     23` 
		returns ['01', '56.7', '23']
		instead of
		['01', '', '56.7', '', '23']
	"""
	parts = line.split()
	ret = []
	for p in parts:
		if p != "":
			ret.append(p)
	return ret

ICAO_MATCH = '[A-Z]{4}'
"""Airport elimination convenience and only 'major' icao airport, none small strips all over the places et desert, jungle, outback et all.
   eg EGLL vs EG3 vs EGE4 - only first one is ICAO ;-)

	Regular expression to match all upper letters only in capitals, no numbers or shorter than four allowed"""

ICAO_MATCH_RE_COMPILED = re.compile(ICAO_MATCH)
"""Precompiled expression"""


def is_icao(code):
	"""Returns True is code matches `ICAO_MATCH`"""
	res = ICAO_MATCH_RE_COMPILED.match(code)
	return res != None
		
		