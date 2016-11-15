import poplib
mailServer = 'sg55.singhost.net'
emailID = 'yakun@h2i.sg'
emailPass = '_Kobe1747'

## open connection to mail server (Secured using SSL)
myEmailConnection = poplib.POP3_SSL(mailServer)
## print the response message from server
print myEmailConnection.getwelcome()
## set email address
myEmailConnection.user(emailID)
## set password 
myEmailConnection.pass_(emailPass)
## get information about the email address
EmailInformation = myEmailConnection.stat()
print "Number of new emails: %s (%s bytes)" % EmailInformation
## Reading an email
print "\n\n===\nRead messages\n===\n\n"
 
## Read all emails
numberofmails = EmailInformation[0]
for i in range(80):
	for email in myEmailConnection.retr(i+1)[1]:
		print email