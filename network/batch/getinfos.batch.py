"""imports"""
from commands import *
from time import sleep

"""constantes"""

status,output = getstatusoutput('pwd')

CONST_IP_FILE_PATH = './network/tmp/'
CONST_IP_FILE_NAME = 'iplist.info'
CONST_MAC_FILE_PATH = './network/tmp/'
CONST_MAC_FILE_NAME = 'maclist.info'

"""fonctions"""

def run_command(cmd,info):

	if(info==str('mac')):
		path = CONST_MAC_FILE_PATH
		file = CONST_MAC_FILE_NAME
		status,output = getstatusoutput('ls -l %s | grep %s' % (path,file))
		
		if(status==0):
			status,output = getstatusoutput('rm -f %s%s' % (path,file))
			status,output = getstatusoutput('touch %s%s' % (path,file))
		else:
			status,output = getstatusoutput('touch %s%s' % (path,file))
	elif(info==str('ip')):
		path = CONST_IP_FILE_PATH
		file = CONST_IP_FILE_NAME
		status,output = getstatusoutput('ls -l %s | grep %s' % (path,file))
		if(status==0):
			print("GETINFOS:replace ip file.")
			status,output = getstatusoutput('rm -f %s%s' % (path,file))
			print("GETINFOS:replace ip file:rm-f:output:%s:status:%s" % (output,status))
			status,output = getstatusoutput('touch %s%s' % (path,file))
			print("GETINFOS:replace ip file:touch:output:%s:status:%s" % (output,status))
		else:
			print("GETINFOS:create ip file.")
			status,output = getstatusoutput('touch %s%s' % (path,file))
			print("GETINFOS:create ip file:touch:output:%s:status:%s" % (output,status))
	else:
		return 1

	elemlist = list()

	status,output = getstatusoutput(cmd)
	print("GETINFOS:run ip search:output:%s:status:%s" % (output,status))
	resultlist = str(output).split("\n")

	for lease in resultlist:
		if lease not in elemlist:
			elemlist.append(lease)

	for elem in elemlist:
		elem = elem.split(';')[0]
		status,output = getstatusoutput("echo '%s' >> %s%s" % (elem,path,file))
		print("GETINFOS:file path:%s%s" % (path,file))
		print("GETINFOS:add %s in file:output:%s:status:%s" % (elem,output,status))

	return 0

print("GETINFOS:start.")
iplist = run_command('nmap -sn 10.0.0.10-49 | grep 10.0.0 | awk -F\" \" \'{print $5}\'',"ip")
#maclist = run_command('cat %s%s | grep \"hardware ethernet\" | awk -F\" \" \'{print $3}\'' % (CONST_DHCP_LEASES_PATH,CONST_DHCP_LEASES_NAME),str('mac'))
print("GETINFOS:end.")
