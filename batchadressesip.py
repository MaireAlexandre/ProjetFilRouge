#imports

from commands import *
from time import sleep

#constante
FILEPATH = '/home/webadmin/Documents/filrouge/'
FILENAME = 'IpList.info'
DHCPLEASESPATH = './'
DHCPLEASESNAME = 'dhcpd.leases'

#fonctions

def run_command(cmd):
	
	ipList = list()
		
	status, result = getstatusoutput(cmd)
	resultlist = str(result).split("\n")

	for lease in resultlist:
#		print(lease not in ipList)
		if lease not in ipList:
			ipList.append(lease)
	
	status = getstatus('ls -l %s | grep %s' % (FILEPATH,FILENAME))
	if status is not 0:
		result = getoutput('touch %s%s' % (FILEPATH,FILENAME))
  
	for ip in ipList:
		status, result = getstatusoutput('echo %s >> %s%s' % (str(ip),FILEPATH,FILENAME))

#main
#sleep(10)
list = run_command('cat %s%s | grep lease | awk -F\" \" \'{print $2}\'' % (DHCPLEASESPATH,DHCPLEASESNAME))
