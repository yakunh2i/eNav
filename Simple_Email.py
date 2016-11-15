#!/usr/bin/python

import smtplib
import smtpd

sender = 'yakun@h2i.sg'
receivers = ['leon4one@gmail.com']

user = r"yakun@h2i.sg"
pwd = r""


message = """From: yakun@h2i.sg
To: leon4one@gmail
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
	smtpObj = smtplib.SMTP('mail.h2i.sg')
	smtpObj.login(user,pwd)
	smtpObj.sendmail(sender, receivers, message)         
	print "Successfully sent email"
except SMTPException:
	print "Error: unable to send email"