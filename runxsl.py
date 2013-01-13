#!/usr/bin/python

"""Apply the specifed xsl file to the xml file and
print out the results

Usage:
  runxsl.py [options] XSL_FILE XML_FILE

Options:
  -h --help     Show this help message and exit

"""
from docopt import docopt
from lxml import etree

if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        xsl_file = args['XSL_FILE']
        xml_file = args['XML_FILE']
    except KeyError:
        print(__doc__)
        exit(1)

    xsl_doc = etree.XSLT(etree.parse(open(xsl_file, 'r')))
    xml_doc = etree.parse(open(xml_file, 'r'))
    output_doc = xsl_doc(xml_doc)
    print(etree.tostring(output_doc, encoding='UTF-8', pretty_print=True))

