#!/usr/bin/python

import os, os.path
import string, re
import sys, subprocess
import time
import email, getpass, imaplib
import zipfile, gzip
import json
import urllib2
import logging
import logging.handlers
from datetime import datetime
from ConfigParser import ConfigParser
import SMTP_send

svdir = './'
FD = ','

for filename in SMTP_send.getfiles(svdir):
	fullfilename = os.path.join(svdir,filename)
	fullfilename = os.path.abspath(fullfilename)
	if(fullfilename.endswith('.txt') or fullfilename.endswith('.req')):
		#print 'request text file: ' +  fullfilename
		lines = [line.rstrip('\n') for line in open(fullfilename)]
		#lines = ['1', '92,-0.1,124.41,32.5,0.4,2016-11-04,2016-11-05', '2', 'tidall,64,eNavHydro/U10,eNavHydro/V10', 'water,64,eNavHydro/s1', '2455,2456,2537,2538,2619,2700,2701', '2782,2783,2863,2864', '']
		req_info = lines[1].split(FD)
		req_type_number = lines[2]
		ln = 0
		while ln < req_type_number:
			
			ln += 1
			
		west=lines[1,0];south=$2;east=$3;north=$4;tileSize=$5;bdate=$6;edate=$7;
		
		
		
		
		
		
		
		uri="http://dev.h2i.sg/ncWMS/wms?request=GetUTFGrid&digits=2&crs=CRS:84"
		
		
		
		#logger.info('Converting the request file ' + fullfilename + ' to list of urls')
		os.system(r'awk -f ' + awk_formatter + ' "' + fullfilename + '"' + ' &> '  + os.path.join(os.path.dirname(fullfilename),'curls.log'))

		lines = [line.rstrip('\n') for line in open(os.path.join(os.path.dirname(fullfilename),'curls.log'))]
		for line in lines:
			curls_vars = re.match(r"^curl \"(http.*)\"\s-o\s(.*\.json)$",line)
			print str(curls_vars)
			req_url = curls_vars.group(1)
			json_file = os.path.join(os.path.dirname(fullfilename),curls_vars.group(2))
			try:
				#logger.info('Sending request : ' + req_url)
				resp = urllib2.urlopen(req_url)
			except:
				#logger.error('Problem in getting response for : ' + req_url)
				continue
			data = resp.read()
			with open(json_file,'wb') as outfile:
				json.dump(data,outfile)
			outfile.close()