"""imports"""
from commands import *
from time import sleep

"""constantes"""

status,output = getstatusoutput('pwd')

CONST_IP_FILE_PATH = output + '/../tmp/'
CONST_IP_FILE_NAME = output + 'iplist.info'
CONST_MAC_FILE_PATH = output + '/../tmp/'
CONST_MAC_FILE_NAME = output + 'maclist.info'
CONST_DHCP_LEASES_PATH = output + '/var/lib/dhcp/'
CONST_DHCP_LEASES_NAME = output + 'dhcpd.leases'

"""fonctions"""

def run_command(cmd,info):
	
	if(info==str('mac')):
		path = CONST_MAC_FILE_PATH
		file = CONST_MAC_FILE_NAME
		status,output = getstatusoutput('ls -l %s%s | grep %s' % (path,file,file))
		if(status==0):
			status,output = getstatusoutput('rm %s%s' % (path,file))
			status,output = getstatusoutput('touch %s%s' % (path,file))
		else:
			status,output = getstatusoutput('touch %s%s' % (path,file))
	elif(info==str('ip')):
		path = CONST_IP_FILE_NAME
		file = CONST_IP_FILE_NAME
		status,output = getstatusoutput('ls -l %s%s | grep %s' % (path,file,file))
		if(status==0):
			status,output = getstatusoutput('rm %s%s' % (path,file))
			status,output = getstatusoutput('touch %s%s' % (path,file))
		else:
			status,output = getstatusoutput('touch %s%s' % (path,file))
	else:
		return 1

	elemlist = list()
	
	status,output = getstatusoutput(cmd)
	resultlist = str(output).split("\n")
	
	for lease in resultlist:
		if lease not in elemlist:
			elemlist.append(lease)
	
	status = getstatus('ls -l %s | grep %s' % (path,file))
	if status is not 0:
		status,output = getstatusoutput('touch %s%s' % (path,file))
	
	for elem in elemlist:
		elem = elem.split(';')[0]
		status,output = getstatusoutput("echo '%s' >> %s%s" % (path,file))
	
	return 0

iplist = run_command('cat %s%s | grep 10.0.0 | awk -F\" \" \'{print $2}\'' % (CONST_DHCP_LEASES_PATH,CONST_DHCP_LEASES_NAME),str('ip'))
maclist = run_command('cat %s%s | grep \"hardware ethernet\" | awk -F\" \" \'{print $3}\'' % (CONST_DHCP_LEASES_PATH,CONST_DHCP_LEASES_NAME),str('mac'))