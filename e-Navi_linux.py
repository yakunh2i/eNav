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



def assure_dir_exists(dir):
	absdir = os.path.abspath(dir)
	if not os.path.exists(absdir):
		try:
			print 'Creating local directory: ' + absdir + '\n'
			os.makedirs(absdir, 0755)
		except:
			print 'Cannot create local directory: ' + absdir + '\n'
			sys.exit(2)

def main():
	if len(sys.argv) < 1:
		print ("Usage: e-Navi_linux ConfigFilePath")

	else:
		ConfigFilePath = sys.argv[1]

		#initialization, reading config file
		parser = ConfigParser()
		print ConfigFilePath
		parser.read(ConfigFilePath)
		#print os.path.join(os.path.abspath('.'),ConfigFilePath)
		#parser.read(os.path.join(os.path.abspath('.'),ConfigFilePath)


		#set up logger
		logfile = parser.get('Path_Info', 'logfile')
		logdir = parser.get('Path_Info', 'logdir')
		assure_dir_exists(logdir)
		logger = logging.getLogger("e-Navi_email")
		logger.setLevel(logging.DEBUG)

		# create console handler and set level to debug
		ch = logging.handlers.RotatingFileHandler(logfile,maxBytes=200000, backupCount=5)
		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)

		# create formatter
		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

		# add formatter to ch
		console.setFormatter(formatter)
		ch.setFormatter(formatter)

		# add ch to logger
		logger.addHandler(ch)
		logger.addHandler(console)



		#intermediate location for email attchements
		#svdir = r''
		svdir = parser.get('Path_Info', 'svdir')
		assure_dir_exists(os.path.abspath(svdir))

		#permanent location for email attachments archiving
		#arcdir = r''
		arcdir = parser.get('Path_Info', 'arcdir')
		assure_dir_exists(os.path.abspath(arcdir))

		#path of the .awk formatter file
		awk_formatter = parser.get('Path_Info', 'awk_formatter')
		awk_formatter = os.path.abspath(awk_formatter)

		#user = raw_input("Enter your email username --> ")
		#pwd = getpass.getpass("Enter your password --> ")
		#user = r''
		user = parser.get('Email_Info', 'email')

		#pwd = r''
		pwd = parser.get('Email_Info', 'password')

		#mail_server  = r''
		mail_server = parser.get('Email_Info', 'mail_server')


		#loggin in
		logger.info('Log in to email account ' + user + '\n\n')
		mail=imaplib.IMAP4_SSL(mail_server)
		try:
			mail.login(user,pwd)
		except:
			logger.error('Problem during login to ' + user + '\n\n')
			sys.exit(2)
		mail.select("inbox")



		while True:

			#Find list of UIDs for unread emails
			typ, msgs = mail.search(None, 'UNSEEN')
			msgs = msgs[0].split()


			#Save email attachments
			for emailid in msgs:

				varSubject = r""
				varSender = r""


				#typ, flag_data = mail.fetch(emailid, '(FLAGS)')
				#for response_part in flag_data:
				#	   print '\nFlag is: ' + str(imaplib.ParseFlags(response_part))

				typ, data = mail.fetch(emailid, "(RFC822)")
				for response_part in data:
					if isinstance(response_part, tuple):

						msg_all = email.message_from_string(response_part[1])
						varSubject = str(msg_all['subject'])
						varSender = str(msg_all['from'])
						varSender = re.sub('^.*\<','',varSender)
						varSender = re.sub('\>.*$','',varSender)

						logger.info('Start processing for the email: ' + '"' + varSubject + '"' + ' from ' + varSender)

						m = email.message_from_string(response_part[1])
						if m.get_content_maintype() != 'multipart':
							continue

						for part in m.walk():
							if part.get_content_maintype() == 'multipart':
								continue
							if part.get('Content-Disposition') is None:
								continue

							filename=part.get_filename()
							#filename=re.sub('\s+','_',filename)
							#filename=re.sub('[()]','',filename)
							if filename is not None:
								sv_path = os.path.join(svdir, filename)
								sv_path = os.path.abspath(sv_path)
								if not os.path.isfile(sv_path):

									#print 'sv_path is ' +  str(sv_path)
									try:
										logger.info('Attempting to saving attachment to local file: ' + sv_path)
										fp = open(sv_path, 'wb')
										fp.write(part.get_payload(decode=True))

									except:
										logger.error('Problem during saving attachment to local file: ' + sv_path)
										continue
									fp.close()

				#Process email attachments
				#Unzip the .zip & .gzip attachments
				for filename in SMTP_send.getfiles(svdir):
					fullfilename = os.path.join(svdir,filename)
					fullfilename = os.path.abspath(fullfilename)

					if(fullfilename.endswith('.zip')):
						try:
							logger.info('Opening the zipped file: ' + fullfilename)
							zfile = zipfile.ZipFile(fullfilename)
							logger.info('Extracting from the zipped file: ' + fullfilename)
							zfile.extractall(svdir)
							zfile.close()
							logger.info('Unzipped the file: ' + fullfilename)
						except KeyError:
							logger.error('Problem accessing the zipped file ' + fullfilename)
							#print 'ERROR: Unable to open the archive %s ' % fullfilename
							zfile.close()
							continue
						logger.info('Deleting the zipped file: ' + fullfilename + ' after attempting decompression')
						os.unlink(fullfilename)

					if(fullfilename.endswith('.gzip')):
						try:
							logger.info('Opening the gzipped file: ' + fullfilename)
							r_file = gzip.GzipFile(fullfilename, 'rb')
							write_file = string.rstrip(fullfilename, '.gz')
							w_file = open(write_file, 'wb')
							logger.info('Extracting from the gzipped file: ' + fullfilename)
							w_file.write(r_file.read())
							w_file.close()
							r_file.close()
							logger.info('Gunzipped the file: ' + fullfilename)
						except KeyError:
							logger.error('Problem during extracting the gzipped file ' + fullfilename)
							#print 'ERROR: Unable to open the archive %s ' % fullfilename
							w_file.close()
							r_file.close()
							continue
						logger.info('Deleting the gzipped file: ' + fullfilename + ' after attempting decompression')
						os.unlink(fullfilename)

				#Convert the attachments to json files
				for filename in SMTP_send.getfiles(svdir):
					fullfilename = os.path.join(svdir,filename)
					fullfilename = os.path.abspath(fullfilename)
					if(fullfilename.endswith('.txt') or fullfilename.endswith('.req')):
						#print 'request text file: ' +  fullfilename
						logger.info('Converting the request file ' + fullfilename + ' to list of urls')
						os.system(r'awk -f ' + awk_formatter + ' "' + fullfilename + '"' + ' &> '  + os.path.join(os.path.dirname(fullfilename),'curls.log'))

						lines = [line.rstrip('\n') for line in open(os.path.join(os.path.dirname(fullfilename),'curls.log'))]
						for line in lines:
							curls_vars = re.match(r"^curl \"(http.*)\"\s-o\s(.*\.json)$",line)
							print str(curls_vars)
							req_url = curls_vars.group(1)
							json_file = os.path.join(os.path.dirname(fullfilename),curls_vars.group(2))
							try:
								logger.info('Sending request : ' + req_url)
								resp = urllib2.urlopen(req_url)
							except:
								logger.error('Problem in getting response for : ' + req_url)
								continue
							data = resp.read()
							with open(json_file,'wb') as outfile:
								json.dump(data,outfile)
							outfile.close()

						#os.system(r"./req_process.sh");
						#os.system(r'ls -lrth ' + os.path.dirname(fullfilename))

						logger.info('Deleting the original request file and the converted url file')
						os.unlink(os.path.join(svdir,r"curls.log"))
						os.unlink(fullfilename)

				#Zip up the json files before sending email
				ts = datetime.now().strftime('%Y%m%d_%H%M%S')
				my_zipfile = ts+'.json_result.zip'
				my_zipfile = os.path.abspath(os.path.join(svdir,my_zipfile))
				with zipfile.ZipFile(my_zipfile, 'w') as myzip:
					for filename in SMTP_send.getfiles(svdir):
						fullfilename = os.path.join(svdir,filename)
						#fullfilename = os.path.abspath(fullfilename)
						if(filename.endswith('.json')):
							logger.info('Adding the json result file ' + fullfilename + ' to zipped archive')
							myzip.write(fullfilename,os.path.basename(fullfilename))
					myzip.close()

				#Reply with new attachments after processing
				try:
					logger.info('Replying to: ' + varSender + ' with the zipped archive ' + my_zipfile)
					if re.search("^re:",varSubject, re.IGNORECASE):
						#SMTP_send.reply_att(varSubject,user,pwd)
						SMTP_send.reply_att(varSubject,user,pwd,varSender,mail_server,svdir)
					else:
						varSubject = 'Re: '+ varSubject
						#SMTP_send.reply_att(varSubject,user,pwd)
						SMTP_send.reply_att(varSubject,user,pwd,varSender,mail_server,svdir)
				except:
					logger.error('Problem in sending email')
						sys.exit(2)


				#Housekeep download folder
				logger.info('Housekeep download folder ' + os.path.abspath(svdir))
				for filename in SMTP_send.getfiles(svdir):
					fullfilename = os.path.join(svdir,filename)
					fullfilename = os.path.abspath(fullfilename)
					arcdir = os.path.abspath(arcdir)
					logger.info('Deleteing ' + os.path.basename(fullfilename))
					if(fullfilename.endswith('.json_result.zip')):
						os.system(r"mv " + fullfilename + " " + arcdir)
					else:
						os.unlink(fullfilename)


				logger.info('Finished processing for the email: ' + '"' + varSubject + '"' + ' from ' + varSender + '\n')
			time.sleep(60)  # Delay for 1 minute (60 seconds)

		#Done
		mail.logout()


if __name__ == "__main__":
	main()

