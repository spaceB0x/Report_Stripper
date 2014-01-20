Report_Stripper
===============

Python script which Searches through PDF and strips away all info that isn't an email subject line. 
Takes parameters -f <inputfile> (must be a pdf)
                 -w <outputfile> outupt file to write to
                 
Requires the 'pdfminer' library which can be downloaded and installed here:

https://pypi.python.org/pypi/pdfminer/


Also requires the pdf2txt program to reside in same directory as pdfminer, OR somewhere in the system PATH or environment variables. 


TODO:

May expand (upon need) to search for other types of information
Perhaps search through other types of files, not just pdf




Author: Tyler Welton (spaceB0x)
Date: Jan, 20 2014
Version 1.0
