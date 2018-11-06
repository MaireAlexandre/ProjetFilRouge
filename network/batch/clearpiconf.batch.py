import networkx as nx
import pexpect
from commands import *
from time import sleep

"""CONSTANTES - a modifier si necessaire"""

status,output = getstatusoutput('pwd')

CONST_LOG_FILE_PATH = './network/log/'
CONST_LOG_NAME_PATH = 'batch.log'

CONST_GML_FILE_PATH = './uploadFiles/'
CONST_GML_FILE_NAME = 'up.gml'

CONST_INFRA_DPLD = "./network/infradpld"

CONST_USER = 'webadmin'
CONST_PWD = 'webadmin'

CONST_ROOT_PWD = 'root'

CONST_INTERFACES_FILE_PATH = 'interfaces'

"""FONCTION"""
def reset_node(ip):

	co = pexpect.spawn("ssh %s@%s" % (CONST_USER,ip))
	co.expect("%s@%s's password: " % (CONST_USER,ip))
	co.sendline(CONST_PWD)
	co.expect('[#\$]')
	co.sendline("su")
	co.expect("Mot de passe :")
	co.sendline("%s" % CONST_ROOT_PWD)

	i = co.expect(["su : Echec d'authentification",'[#\$]'])

	if(i==1):
		status,output = getstatusoutput("cat %s" % CONST_INFRA_DPLD)
		print("output:%s" % output)
		if(output=="1"):
			print("CLEARPICONF:clear %s" % ip)
			co.sendline("cd /etc/network/")
			co.expect('[#\$]')
			co.sendline("ifdown $(cat interfaces | grep  \"auto eth0.\" | awk -F\" \" '{print $2}')")
			co.expect('[#\$]')
			print("%s.old" % CONST_INTERFACES_FILE_PATH)
			co.sendline("cp %s.old %s" % (CONST_INTERFACES_FILE_PATH,CONST_INTERFACES_FILE_PATH))
			co.expect('[#\$]')
			co.sendline("rm interfaces.old")
			co.expect('[#\$]')
	else:
		#print("ERREUR: echec d'authentication")
		co.kill(0)
		return 1

	co.close()
	return 0

"""MAIN"""

print("CLEARPICONF:start.")

gml_file = nx.read_gml("%s%s" % (CONST_GML_FILE_PATH,CONST_GML_FILE_NAME))
ip_list = nx.get_node_attributes(gml_file, 'ip')

for ip in ip_list:
	reset_node(ip_list[ip])
	print("CLEARPICONF:reset node %s" % ip)

print("CLEARPICONF:end.")
