#!/usr/bin/python

import os, os.path
import string, re
import sys, subprocess
import time
import email, getpass, imaplib
import zipfile, gzip
import json
import urllib2
import math
import logging
import logging.handlers
from datetime import datetime
from ConfigParser import ConfigParser
import SMTP_send

svdir = './attachments'
FD = ','

for filename in SMTP_send.getfiles(svdir):
	fullfilename = os.path.join(svdir,filename)
	fullfilename = os.path.abspath(fullfilename)
	if(fullfilename.endswith('.txt') or fullfilename.endswith('.req')):
		#print 'request text file: ' +  fullfilename
		lines = [line.rstrip('\n') for line in open(fullfilename)]
		print 'before: '+ str(lines)
		#lines = ['1', '92,-0.1,124.41,32.5,0.4,2016-11-04,2016-11-05', '2', 'tidall,64,eNavHydro/U10,eNavHydro/V10', 'water,64,eNavHydro/s1', '2455,2456,2537,2538,2619,2700,2701', '2782,2783,2863,2864', '']
		for line in lines:
			if line == '':
				lines.remove(line)
		
		print 'after: ' + str(lines)
		
		req_info = lines[1].split(FD)
		req_type_number = int(lines[2]) #2
		ln = 0
		data_names = []
		while ln < req_type_number:
			print 'lines[3+ln] ' + lines[3+ln]
			data_names.append(lines[3+ln])
			print 'data_names[ln] ' + data_names[ln] 
			ln += 1
			print ln
		
			
		west=float(req_info[0])
		south=float(req_info[1])
		east=float(req_info[2])
		north=float(req_info[3])
		tileSize=float(req_info[4])
		bdate=req_info[5]
		edate=req_info[6]
		print 'west ' + str(west)
		print 'south ' + str(south)
		print 'east ' + str(east)
		print 'north ' + str(north)
		print 'tileSize ' + str(tileSize)
		print 'bdate ' + str(bdate)
		print 'edate ' + str(edate)
		print 'data_names' + str(data_names)
		
		uri='http://dev.h2i.sg/ncWMS/wms?request=GetUTFGrid&digits=2&crs=CRS:84'
		
		tile_list = []
		ln = 3 + req_type_number
		while ln < len(lines):
			temp_tiles = lines[ln].split(FD)
			for tile in temp_tiles:
				tile_list.append(int(tile))
			ln += 1 
		
		
		print 'tile_list: ' + str(tile_list)
		
		xsize=int(0.5+(east-west)/tileSize)# now it's trunc, not round
		ysize=int(0.5+(north-south)/tileSize)

		
		print xsize
		print ysize
		
		
		get_req = []
		for tile in tile_list:
			#print tile
			dx=int(int(tile)/xsize)
			dy=(int(tile)%ysize)
			for dm in data_names:
				temp_param_list=dm.split(FD)
				
				temp_size = temp_param_list[1]
				
				#print temp_param_list
				layer_idx = 3
				temp_layer = temp_param_list[2] 
				while layer_idx < len(temp_param_list):
					temp_layer += ','
					temp_layer += temp_param_list[layer_idx]
					layer_idx += 1
				#print temp_layer
				
				print (r'curl "'+uri+'&time='+bdate+'T00:00:00Z/'+edate+'T23:30:00Z&layers='+temp_layer+'&size='+temp_size+'&bbox='+str(west+dx*tileSize)+','+str(north-(dy+1)*tileSize)+','+str(west+(dx+1)*tileSize)+','+str(north-dy*tileSize)+'" -o '+temp_param_list[0]+'_'+str(tile)+'.json\n')
				#tile_list.append(r"\"uri&time=bdateT00:00:00Z/edateT23:30:00Z&layers=dm[3]&size=dm[2]&bbox= west+dx*tileSize , north-(dy+1)*tileSize , west+(dx+1)*tileSize , north-dy*tileSize \" -o  dm[1]_tile .json\n")
				get_req.append(r'curl "'+uri+'&time='+bdate+'T00:00:00Z/'+edate+'T23:30:00Z&layers='+temp_layer+'&size='+temp_size+'&bbox='+str(west+dx*tileSize)+','+str(north-(dy+1)*tileSize)+','+str(west+(dx+1)*tileSize)+','+str(north-dy*tileSize)+'" -o '+temp_param_list[0]+'_'+str(tile)+'.json\n')
		
		print len(get_req)
		print get_req
		
		#logger.info('Converting the request file ' + fullfilename + ' to list of urls')
		"""
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
			"""