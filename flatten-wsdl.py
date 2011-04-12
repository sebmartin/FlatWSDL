#! /usr/bin/python

import xml.etree.ElementTree as etree
import urllib


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
		
		#	if importEl.tag == '{http://www.w3.org/2001/XMLSchema}import':
		#		import pdb; pdb.set_trace()
		
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


def flattenWsdl(url):
	tree = loadTreeFromUrl(url)
	root = tree.getroot()
	
	# Process WSDL imports
	flattenImports(root, '{http://schemas.xmlsoap.org/wsdl/}import', [])
	
	# Process XSD imports
	for schema in root.findall('.//{http://www.w3.org/2001/XMLSchema}schema'):
		flattenImports(schema, '{http://www.w3.org/2001/XMLSchema}import', [])
	
	tree.write('./test.xml')


flattenWsdl('<insert-url-to-wsdl-here>')

print "done."
