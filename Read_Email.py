import email, getpass, imaplib, os, re
import mailbox

detach_dir = r"C:\Users\hp\Desktop\e-Navi\attachments"  


user = raw_input("Enter your email username --> ")
pwd = getpass.getpass("Enter your password --> ")


m = imaplib.IMAP4_SSL("sg55.singhost.net")
m.login(user, pwd)

my_msg = []

m.select("Inbox")

resp, items = m.search(None, '(FROM "yakun@h2i.sg")')

items = items[0].split()
#['3', '31', '32', '33', '36', '54', '55', '56', '57', '58', '60', '80']

#for emailid in items[::-1]:
#
#	resp, data = m.fetch(emailid, "(RFC822)")
#	
#	for response_part in data:
#
#		if isinstance(response_part, tuple):
#			msg = email.message_from_string(response_part[1])
#			varSubject = msg['subject']
#			varDate = msg['date']
#
#			r, d = m.fetch(emailid, "(UID BODY[TEXT])")
#
#			ymd = email.utils.parsedate(varDate)[0:3]
#			my_msg.append([ email.message_from_string(d[0][1]) , ymd ])
#			print '\n' + str(ymd) + '\n'

#for num in items[0].split():
#	typ, data = m.fetch(num, '(UID BODY[TEXT]')
#	print 'Message %s\n%s\n' % (num, data[0][1])

#print data[1]

b = str(m.fetch(items[len(items)-1], "(RFC822)")[1])
	
b = email.message_from_string(b)
print str(b.get_payload())

body = ""

#if b.is_multipart():
#	for part in b.walk():
#		ctype = part.get_content_type()
#		cdispo = str(part.get('Content-Disposition'))
#
#        # skip any text/plain (txt) attachments
#		if ctype == 'text/plain' and 'attachment' not in cdispo:
#			body = part.get_payload(decode=True)  # decode
#			break
#			
#	print str(body)
## not multipart - i.e. plain text, no attachments, keeping fingers crossed
#else:
#	body = b.get_payload(decode=True)
#	print 'NONE'


#if b.is_multipart():
#	for payload in b.get_payload():
#		print str(payload.get_payload())
#else:
#	print str(b.get_payload())