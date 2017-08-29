# Checking-rm-process-UNIX

This Script Checks any "rm" command running on the System and analyse if its running more than a minute,hour and day then capture and stores into a file in /tmp Directory (/tmp/ps_msg), this output further encapsulated and used by sendmail to send the e-mails to the desired recipients. Once mails program finished out it unlinks the file from "/tmp" and whole program closed.
