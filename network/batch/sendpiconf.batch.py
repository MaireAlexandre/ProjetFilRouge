import networkx as nx
import pexpect
from commands import *
from time import sleep

"""CONSTANTES - a modifier si necessaire"""

status,output = getstatusoutput('pwd')

CONST_INFRA_DPLD = './network/infradpld'

CONST_LOG_FILE_PATH = './network/log/'
CONST_LOG_NAME_PATH = 'batch.log'

CONST_IP_FILE_PATH = './network/tmp/'
CONST_IP_FILE_NAME = 'iplist.info'

CONST_GML_FILE_PATH = './uploadFiles/'
CONST_GML_FILE_NAME = 'up.gml'

CONST_USER = 'webadmin'
CONST_PWD = 'webadmin'

CONST_ROOT_PWD = 'root'

CONST_INTERFACES_FILE_PATH = '/etc/network/interfaces'

CONST_NETWORK_BYTE_1 = '10'
CONST_NETWORK_BYTE_2 = '0'
CONST_NETWORK_BYTE_4_1 = '1'
CONST_NETWORK_BYTE_4_2 = '2'

CONST_VLAN_NETMASK = "255.255.255.0"

"""VARIABLES GLOBALES"""

#GLOBAL_LAST_VLAN_NUM = 0
GLOBAL_INCREMENT = 10

"""FONCTION"""
def configure_node(ip):

	co = pexpect.spawn("ssh %s@%s" % (CONST_USER,ip))
	co.expect("%s@%s's password: " % (CONST_USER,ip))
	co.sendline(CONST_PWD)
	co.expect('[#\$]')
	co.sendline("su")
	co.expect("Mot de passe :")
	co.sendline("%s" % CONST_ROOT_PWD)

	i = co.expect(["su : Echec d'authentification",'[#\$]'])

	if(i==1):
		co.sendline("modprobe 8021q")
		co.expect('[#\$]')
		co.sendline("cp %s %s.old" % (CONST_INTERFACES_FILE_PATH,CONST_INTERFACES_FILE_PATH))
		co.expect('[#\$]')
	else:
		#print("ERREUR: echec d'authentication")
		co.kill(0)
		return 1

	co.close()
	return 0


def configure_link(ip1,ip2,vlanNumber):

	#print("GLOBAL_INCREMENTAL_VLAN_NUMBER = %s" % str(GLOBAL_INCREMENT))
	configure_vlan(ip1,1,vlanNumber)
	#print('configure_node1 %s' % ip1)
	configure_vlan(ip2,2,vlanNumber)
	#print('configure_node1 %s' % ip2)

def configure_vlan(ip,last_byte,vlanNumber):

	co = pexpect.spawn("ssh %s@%s" % (CONST_USER,ip))
	co.expect("%s@%s's password: " % (CONST_USER,ip))
	co.sendline(CONST_PWD)
	co.expect('[#\$]')
	co.sendline("su")
	co.expect("Mot de passe :")
	co.sendline("%s" % CONST_ROOT_PWD)

	i = co.expect(["su : Echec d'authentification",'[#\$]'])

	if(i==1):
		co.sendline("echo '' >> %s" % CONST_INTERFACES_FILE_PATH)
		co.expect('[#\$]')
		co.sendline("echo 'auto eth0.%s' >> %s" % (vlanNumber,CONST_INTERFACES_FILE_PATH))
		co.expect('[#\$]')
		co.sendline("echo 'iface eth0.%s inet static' >> %s" % (vlanNumber,CONST_INTERFACES_FILE_PATH))
		co.expect('[#\$]')

		addr_vlan = 0
		if(last_byte==2):
			addr_vlan = str(CONST_NETWORK_BYTE_1)+"."+str(CONST_NETWORK_BYTE_2)+"."+str(vlanNumber)+"."+str(CONST_NETWORK_BYTE_4_1)
		elif(last_byte==1):
			addr_vlan = str(CONST_NETWORK_BYTE_1)+"."+str(CONST_NETWORK_BYTE_2)+"."+str(vlanNumber)+"."+str(CONST_NETWORK_BYTE_4_2)
		else:
			return 1

		co.sendline("echo 'address %s' >> %s" % (addr_vlan,CONST_INTERFACES_FILE_PATH))
		co.expect('[#\$]')
		co.sendline("echo 'netmask %s' >> %s" % (CONST_VLAN_NETMASK,CONST_INTERFACES_FILE_PATH))
		co.expect('[#\$]')
		co.sendline('ifup eth0.%s' % vlanNumber)
		co.expect('[#\$]')
	else:
		#print("ERREUR: echec d'authentication")
		co.kill(0)
		print("echo '1' > %s" % CONST_INFRA_DPLD)
		return 1

	co.close()
	return 0

"""MAIN"""

gml_file = nx.read_gml("%s%s" % (CONST_GML_FILE_PATH,CONST_GML_FILE_NAME))
ip_list = nx.get_node_attributes(gml_file, 'ip')

for ip in ip_list:
	configure_node(ip_list[ip])

edges = gml_file.edges()

vlanNumber = GLOBAL_INCREMENT
for elem in edges:
	#print("source : %s" % ip_list[elem[0]])
	#print("target : %s" % ip_list[elem[1]])
	configure_link(ip_list[elem[0]],ip_list[elem[1]],vlanNumber)
	vlanNumber += GLOBAL_INCREMENT

status,output = getstatusoutput("echo '1' > %s" % CONST_INFRA_DPLD)
