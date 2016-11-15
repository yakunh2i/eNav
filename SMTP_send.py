import smtplib
import os, os.path
import string,re
import sys, subprocess
import email
import mimetypes
import gzip

# Here are the email package modules we'll need
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.message import Message



def getfiles(dirpath):
	a = [s for s in os.listdir(dirpath)
		if os.path.isfile(os.path.join(dirpath, s))]
	a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
	return a


def reply_att(subject_str,user,pwd,to_addr,server,svdir):
	COMMASPACE = ';'

	# Send the email via our own SMTP server.
	#s = smtplib.SMTP('sg55.singhost.net')
	#s = smtplib.SMTP('mail.h2i.sg')
	s = smtplib.SMTP(server)
	s.login(user,pwd)

	#svdir = r"./attachments"

	# Create the container (outer) email message.
	outer = MIMEMultipart()
	outer['Subject'] = subject_str
	#sender = 'yakun@h2i.sg'
	sender = user
	receiver_addr = [to_addr]
	outer['From'] = sender
	outer['To'] = COMMASPACE.join(receiver_addr)
	outer.preamble = ''



	# Assume that the attachment to be sent is .zip format
	for filename in getfiles(svdir):
		if(filename.endswith('.zip')):
			fullfilename = os.path.join(svdir,filename)
			fullfilename = os.path.abspath(fullfilename)
			# Guess the content type based on the file's extension.  Encoding
			# will be ignored, although we should check for simple things like
			# gzip'd or compressed files.
			ctype, encoding = mimetypes.guess_type(fullfilename)
			if ctype is None or encoding is not None:
				# No guess could be made, or the file is encoded (compressed), so
				# use a generic bag-of-bits type.
				ctype = 'application/octet-stream'
			maintype, subtype = ctype.split('/', 1)
			'''if maintype == 'text':
				with open(fullfilename) as fp:
					# Note: we should handle calculating the charset
					msg = MIMEText(fp.read(), _subtype=subtype)
			elif maintype == 'image':
				with open(fullfilename, 'rb') as fp:
					msg = MIMEImage(fp.read(), _subtype=subtype)
			elif maintype == 'audio':
				with open(fullfilename, 'rb') as fp:
					msg = MIMEAudio(fp.read(), _subtype=subtype)
			else:
			'''
			with open(fullfilename, 'rb') as fp:
				msg = MIMEBase(maintype, subtype)
				msg.set_payload(fp.read())
			# Encode the payload using Base64
			encoders.encode_base64(msg)

			# Set the filename parameter
			msg.add_header('Content-Disposition', 'attachment', filename=filename)
			outer.attach(msg)
			
	# Now send or store the message
	composed = outer.as_string()
	s.sendmail(sender, receiver_addr, composed)
	s.quit()