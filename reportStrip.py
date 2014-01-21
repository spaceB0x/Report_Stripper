
################################################################################
#
# Report Stripper
# reportStrip.py
#
# author:Tyler Welton (aka spaceB0x)
# Jan. 20,2013
# 
# Simple little program
# Takes an input pdf, and searches for line containing "Subject" information
# Then outputs a list of found items to a file.
#
# Utilizes the tool pdf2txt.py included in "pdfminer" module (Thanks)
# 
################################################################################


import os
import optparse

def main():

	####description###
	desc= """Report Stripper takes user specified pdf with -f and looks for the line "Subject: " and then outputs the content to text file. It requires the 'pdfminer' module as well as the pdf2txt tool, either installed in the same directory as reportStrip.py or in the system PATH."""

	#### Setting up Options ####
	parser=optparse.OptionParser("%prog "+ "-f <file> -w <outputfile>", description=desc)
	parser.add_option('-f', dest='filename', type='string', help='Choose the input file')
	parser.add_option('-w', dest='output', type='string',help='Choose file to write results to')
	(options, args)= parser.parse_args()

	#Check for args
	if ((options.filename==None) | (options.output==None)):
		os.system('reportStrip.py --help')
		exit(0)

	###Open Files###
	temp = open('temp.txt', 'rb')
	wfile = open(options.output,"w")
	os.system('pdf2txt.py -o temp.txt %s' % options.filename)

	
	###STRIP###
	print 'Parsing.....'
	for line in temp:
  		if (line.find('Subject:') != -1):
			wfile.write(line.lstrip("Subject:").replace('!', ' ') +"\n")
		
	
	print '\n DONE!'
	temp.close()
	wfile.close()
	
	exit(0)


if __name__=='__main__':
	main()

