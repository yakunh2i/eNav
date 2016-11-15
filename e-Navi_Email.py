import imaplib
import email
import os
import os.path
import string
import sys, subprocess
import string
import email, getpass, imaplib, os, re
import SMTP_send


def Unzip(file, bindir):
	subprocess.call(r'"C:\\Program Files\\7-Zip\7z.exe" x ' + file + ' -o' + bindir + ' -aoa')


#intermediate location for email attchements
svdir = r"C:\Users\hp\Desktop\e-Navi\attachments"

#permanent location for email attachments archiving
arcdir = r"C:\Users\hp\Desktop\e-Navi\archives"


#user = raw_input("Enter your email username --> ")
pwd = getpass.getpass("Enter your password --> ")
user = r"yakun@h2i.sg"
#pwd = r""


#Loggin in
mail=imaplib.IMAP4_SSL('sg55.singhost.net')
mail.login(user,pwd)
mail.select("inbox")

#Find list of UIDs for unread emails
typ, msgs = mail.search(None, 'UNSEEN', '(FROM "yakun@h2i.sg")')
msgs = msgs[0].split()
#print msgs[len(msgs)-1]

varSubject = []

#Save email attachments
for emailid in msgs:

	#typ, flag_data = mail.fetch(emailid, '(FLAGS)')
	#for response_part in flag_data:
	#	print '\nFlag is: ' + str(imaplib.ParseFlags(response_part))

	typ, data = mail.fetch(emailid, "(RFC822)")
	for response_part in data:	
		if isinstance(response_part, tuple):
		
			msg_all = email.message_from_string(response_part[1])
			varSubject.append(str(msg_all['subject']))
			#print '\nSubject is: ' + str(varSubject)
			#if (str(varSubject) == r'Re: client key'):

			m = email.message_from_string(response_part[1])		
			if m.get_content_maintype() != 'multipart':
				continue
			
			for part in m.walk():
				if part.get_content_maintype() == 'multipart':
					continue
				if part.get('Content-Disposition') is None:
					continue
				
				filename=part.get_filename()
				if filename is not None:
					sv_path = os.path.join(svdir, filename)
					if not os.path.isfile(sv_path):
						print str(sv_path)
						
						sv_path = str(sv_path)
						
						fp = open(sv_path, 'wb')
						fp.write(part.get_payload(decode=True))
						fp.close()

							
#Process email attachments
#Unzip the attachments
for filename in getfiles(svdir):
	if(filename.endswith('.zip')):
		fullfilename = svdir + '/' + filename
		Gunzip(fullfilename, svdir)

for filename in getfiles(svdir):
	if(filename.endswith('.bin') and convert):
		fullfilename = svdir + '/' + filename
		convertfile_TRMM(fullfilename,"RAIN",True,convdir,verbose, start_x, end_x, start_y, end_y)
	
	
#Reply with new attachments after processing
for subj in varSubject:
	if re.search("^re:",subj, re.IGNORECASE):	
		SMTP_send.reply_att(subj,user,pwd)
	else:
		subj = 'Re: '+ subj
		SMTP_send.reply_att(subj,user,pwd)


#Move attachments to permanent location for archiving


#Done
mail.logout()