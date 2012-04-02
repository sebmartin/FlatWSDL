#! /usr/bin/python
import sys
import xml.etree.ElementTree as etree
import urllib
from optparse import OptionParser
from subprocess import call

# List of URL to skip
url_skiplist = []

def importUrl(url, parent, after):
	insertOffset = 1
	toFlatten = loadTreeFromUrl(url)
	for child in toFlatten.getroot():
		parent.insert(parent.getchildren().index(after) + insertOffset, child)
		insertOffset += 1

def flattenImports(parent, tag):
 	while True:
		importEl = parent.find(tag)
		if importEl == None:
			break
		
		# Get URL from location or schemaLocation tag
		url = importEl.get('location')
		if not url:
			url = importEl.get('schemaLocation')
		if not url:
			return

		# Import the URLs found and replace their content with the import line
		if not url in url_skiplist:
			if options.verbose:
				print('Importing URL: ' + url)
			importUrl(url, parent, importEl)
			url_skiplist.append(url)
		parent.remove(importEl)

def loadTreeFromUrl(url):
	fp = urllib.urlopen(url)
	tree = etree.parse(fp)
	return tree


def flattenWsdl(url, output):
	tree = loadTreeFromUrl(url)
	root = tree.getroot()
	
	# Process WSDL imports
	flattenImports(root, '{http://schemas.xmlsoap.org/wsdl/}import')
	
	# Process XSD imports
	for schema in root.findall('.//{http://www.w3.org/2001/XMLSchema}schema'):
		flattenImports(schema, '{http://www.w3.org/2001/XMLSchema}import')
	
	tree.write(output)
	
# Process command line arguments
usage = "usage: %prog [options] URL"
parser = OptionParser(usage)
parser.add_option('-f', '--filename', action="store", type="string", dest="filename",
	help='Output file to write to')
parser.add_option('-n', '--namespace', action="store", type="string", dest="namespace",
	help='Override the default namespace')
parser.add_option('-t', '--tidy', action="store_true",
	help='Run |tidy| on the file after flattening. Requires -f')
parser.add_option('-v', '--verbose', action="store_true", help='Enable verbose output')
(options, args) = parser.parse_args()

if options.namespace:
	print('WARNING: the NAMESPACE option is not yet implemented.')

if (len(args) == 0) or ((not options.filename) and options.tidy):
	parser.print_help()
	sys.exit()

out = open(options.filename, 'w+') if options.filename else sys.stdout

# Flatten the WSDL!
try:
	flattenWsdl(args[0], out)
finally:
	print "Flattening done."
	out.close()

if options.tidy:
	tidy_args = ['tidy', '-mi', '-xml', options.filename]
	if not options.verbose:
		tidy_args.insert(1, '-q')
	call(tidy_args)
