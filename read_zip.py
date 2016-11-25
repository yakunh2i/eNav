import os, os.path, io
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


svdir = './attachments'
arcdir = './archives'
logdir = './log'
logfile = './log/email_script.log'

i=0
lines=''
FD=','
for filename in SMTP_send.getfiles(svdir):
	fullfilename = os.path.join(svdir,filename)
	fullfilename = os.path.abspath(fullfilename)
	#print fullfilename
	if(fullfilename.endswith('.zip')):
		try:
			#logger.info('Attempting to saving attachment to local file: ' + sv_path)
			
			zfile = zipfile.ZipFile( fullfilename, 'r')
			for finfo in zfile.namelist():
				print finfo
				ifile = zfile.read(finfo)
		
				#bytes_io = io.BytesIO(ifile)
				print '+++++++++++ UPPER ++++++++++++'					
				print ifile
				print '+++++++++++ UNDER ++++++++++++'
				#print bytes_io

				#ifile is the raw content of the text based request file
				#convert the request file to http requests
				lines = ifile.split('\n')
				for line in lines:
#						print line
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
				
						print (r'curl "'+uri+'&time='+bdate+'T00:00:00Z/'+edate+'T23:30:00Z&layers='+temp_layer+'&size='+temp_size+'&bbox='+str(west+dx*tileSize)+','+str(north-(dy+1)*tileSize)+','+str(west+(dx+1)*tileSize)+','+str(north-dy*tileSize)+'" -o '+temp_param_list[0]+'_'+str(tile)+'.json')
						

				

		except:
			#print "ERROR"
			#logger.error('Problem during saving attachment to local file: ' + sv_path)
			continue
			#fp.close()