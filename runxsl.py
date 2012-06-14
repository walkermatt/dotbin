#!/usr/bin/python

"""Usage: runxsl.py -h --help xsl_file xml_file

Apply the specifed xsl file to the xml file and
print out the results

Options:
  -h --help     Show this help message and exit

"""
from docopt import docopt
from lxml import etree

opts, args = docopt(__doc__)

if (len(args)) < 2:
    print(__doc__)
    exit(1)

xsl_file = args[0]
xml_file = args[1]

xsl_doc = etree.XSLT(etree.parse(open(xsl_file, 'r')))
xml_doc = etree.parse(open(xml_file, 'r'))
output_doc = xsl_doc(xml_doc)
print(etree.tostring(output_doc, encoding='UTF-8', pretty_print=True))
