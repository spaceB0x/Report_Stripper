
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
import re

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
	f = ("%s.txt" % str(options.output)) #append '.txt.'
	wfile = open(f,'w')
	rfile= options.filename 
	print 'Parsing.....'
	os.system('python pdf2txt.py -o temp.txt "%s"' %rfile)
	
	temp = open('temp.txt','rb')
	
	###STRIP###
	
	wfile.write('Suspicious Subject lines: \n')             #write Subject list
	for line in temp:
  		if (line.find('Subject:') != -1):
				wfile.write(line.lstrip("Subject:").replace('!', ' '))			
	temp.close()
	temp = open('temp.txt', 'rb')
							
	wfile.write('\n\n\n	Formatted for Mimecast:\n')				#write formatted list for mimecast
	fmtString = ''
	for line in temp:
		if (line.find('Subject:') != -1):
				fmtString=(fmtString +'"'+(line.lstrip("Subject:").lstrip('\n').lstrip('\r').replace('!',' ')) +'"'+' OR ')
	wfile.write('%s' % fmtString)
	temp.close()
	temp = open('temp.txt', 'rb')

	wfile.write('\n\n\n')									#print IPs using regex
	wfile.write('Suspicious IP addresses: \n')
	for line in temp:
		foundIPs = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
		if foundIPs:
			for ip in foundIPs:
				wfile.write('%s\n' %ip)
	temp.close()
	temp = open('temp.txt', 'rb')
				
	wfile.write('\n\n\n')									#write formatted IPs for SW/Splunk
	wfile.write('IPs Formatted for Splunk: \n')
	for line in temp:
		foundIPs = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
		if foundIPs:
			for ip in foundIPs:
				wfile.write('%s\n' %ip)
	
		
	wfile.write('\n\n\n')									#print Suspect domains.
	wfile.write('Suspicious Domains: \n')
	
	temp.close()
	temp = open('temp.txt', 'rb')
	
	for line in temp:
		domains = re.findall(r'\@?[\w.]+.com',line)
		if domains:
			for d in domains:
				d=d.replace('!','.')
				wfile.write('%s\n' %d)
		
	wfile.write('\n\n\n')									#write formatted for Mimecast
	wfile.write('Domains formatted for Mimecast: \n')		
	
	print '\n DONE!'
	temp.close()
	wfile.close()
	#rfile.close()
	
	exit(0)


if __name__=='__main__':
	main()

