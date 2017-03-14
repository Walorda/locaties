import re
import urllib

try:
	import urllib.request
except:
	pass

sites = "slak".split()
pat = re.compile(r'€\s\d{1,3}', re.I|re.M)

for s in sites:
	print("Searching: " + s)
	try:
		u = urllib.urlopen("http://" + s + ".nl/aanbiedingenlijst/")
	except:
		u = urllib.request.urlopen("http://" + s + ".nl/aanbiedingenlijst/")
	text = u.read()
	title = re.findall(pat, str(text))

	print(title)