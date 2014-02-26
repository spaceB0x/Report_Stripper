
################################################################################
#
# Report Stripper
# reportStrip.py
#
# author:Tyler Welton (aka spaceB0x)
# Jan. 20,2013
# 
# Simple little program
# Takes an input pdf, and searches for line containing "Subject" information from emails
# Also collects any IP address in the document as well as an 'Attempt' at collecting
# domain information
# Then outputs a list of found items to a file.
# Oh yeah, and also formats the info for use in searchcriteria for MimeCast, SPLUNK, etc.
#
# Utilizes the tool pdf2txt.py included in "pdfminer" module (Thanks)
#
# Last Updated: 
################################################################################


import os
import optparse
import re
import time

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
	
	##Declare lists##
	subs=[]
	ips=[]
	domains=[]
	
	
	
	### STRIP ####################################
	##############################################
	
	for line in temp:
		#fill subs[]
		if (line.find('Subject:') != -1):
				subs.append(line.lstrip("Subject:").lstrip("\r\n").replace('!', ' '))			
		#fill ips[]
		foundIPs = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
		if foundIPs:
			for ip in foundIPs:
				ips.append('%s\n' %ip)			
		#fill domains[]
		doms= re.findall(r'\@?[\w]+.com',line)
		if doms:
			for d in doms:
				d=d.replace('!','.')	
				domains.append('%s\n' %d)	
	temp.close()	
		

			
	### PRINT ####################################
	##############################################
	print '\nSuspicious Subject lines: \n'   #write Subject list
	wfile.write('Suspicious Subject lines: \n')
	for s in subs:
		wfile.write(s)
		print s
		
	print '\n\n\nFormatted for Mimecast:\n'				#write subjects formatted list for mimecast
	wfile.write('\n\n\nFormatted for Mimecast:\n')
	fmt=''
	for s in subs:
		sa=s.strip('\r\n')
		sb='"'+sa+'"'+' OR '
		fmt+=sb
	print fmt
	wfile.write(fmt)

	
	print '\n\n\n'							#print IPs using regex
	print 'Suspicious IP addresses: \n'
	wfile.write('\n\n\n')
	wfile.write('Suspicious IP addresses: \n')
	fmt=''
	for i in ips:
		wfile.write(i)
		print i
		
	print '\n\n\n'									#write formatted IPs for SW/Splunk
	print 'IPs Formatted for Splunk: \n'
	wfile.write('\n\n\n')
	wfile.write('IPs Formatted for Splunk: \n')
	fmt=''
	for i in ips:
		sa =i.strip('\r\n')
		sb= sa +' OR '
		fmt+=sb
	print fmt
	wfile.write(fmt)
		
		
	print '\n\n\n'									#print Suspect domains.
	print 'Suspicious Domains: \n'
	wfile.write('\n\n\n')
	wfile.write('Suspicious Domains: \n')
	for d in domains:
		wfile.write(d)
		print d
	
	
	print '\n DONE!'
	wfile.close()
	#rfile.close()
	
	exit(0)


if __name__=='__main__':
	t0=time.clock()
	main()
	print time.clock()-t0
