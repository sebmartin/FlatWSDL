#! /usr/bin/python
import sys
import xml.etree.ElementTree as etree
import urllib
from optparse import OptionParser

def importUrl(url, parent, after):
	insertOffset = 1
	toFlatten = loadTreeFromUrl(url)
	for child in toFlatten.getroot():
		parent.insert(parent.getchildren().index(after) + insertOffset, child)
		insertOffset += 1

def flattenImports(parent, tag, skip):
	
 	while True:
		importEl = parent.find(tag)
		if importEl == None:
			break
			
		url = importEl.get('location')
		if not url:
			url = importEl.get('schemaLocation')
		if not url:
			return
		if not url in skip:
			importUrl(url, parent, importEl)
			skip.append(url)
		parent.remove(importEl)


def loadTreeFromUrl(url):
	fp = urllib.urlopen(url)
	tree = etree.parse(fp)
	return tree


def flattenWsdl(url, output):
	tree = loadTreeFromUrl(url)
	root = tree.getroot()
	
	# Process WSDL imports
	flattenImports(root, '{http://schemas.xmlsoap.org/wsdl/}import', [])
	
	# Process XSD imports
	for schema in root.findall('.//{http://www.w3.org/2001/XMLSchema}schema'):
		flattenImports(schema, '{http://www.w3.org/2001/XMLSchema}import', [])
	
	tree.write(output)
	
# Process command line arguments
parser = OptionParser('usage: %prog [options] URL [file]')
parser.add_option('-n', '--namespace', help='override the default namespace')
(options, args) = parser.parse_args()

if options.namespace:
	print('WARNING: the NAMESPACE option is not yet implemented.')

if len(args) == 0:
	parser.print_usage()
	sys.exit()
elif len(args) > 1:
	out = open(args[1], 'w+')
else:
	out = sys.stdout

# Flatten the WSDL!
try:
	flattenWsdl(args[0], out)
finally:
	print "\ndone."
	out.close()
