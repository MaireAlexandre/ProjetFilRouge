# ProjetSouhi2017
Projet de routage(topologie de r�seau 2017)

#MODIFIEZ LE CHEMIN D'IMPORTATION POUR LE FICHIER

# Cahier des Charges
(A remplir)

# gestion de projet
A definir(AGILE)

# Premiere Partie
Dead linecJanv 2017

Configuration du serveur DHCP (README_conf_DHCP.txt)

#test: je joue avec flask et je fais les IHM Demandé

# Utilisation des scripts réseaux - python2.7

Chaques script utilise des fichiers, des informations contenues dans des fichiers, des nom de comptes et mots de passe etc...
Afin de faciliter leur utilisation, l'ensemble de ces informations sont variabilisées à chaque début de script.
Chacune de ce variables commence par le préfixe "CONST".

NOTE: les variables concernant des répertoires sont basées sur l'emplacement de l'execution du script.

##getinfos.batch.py##

CONST_IP_FILE_PATH = '/../tmp/'
CONST_IP_FILE_NAME = 'iplist.info'
CONST_MAC_FILE_PATH = '/../tmp/'
CONST_MAC_FILE_NAME = 'maclist.info'
CONST_DHCP_LEASES_PATH = '/var/lib/dhcp/'
CONST_DHCP_LEASES_NAME = 'dhcpd.leases'

##sendpiconf.batch.py##

CONST_LOG_FILE_PATH = '/../log/'
CONST_LOG_NAME_PATH = 'batch.log'

CONST_IP_FILE_PATH = '/../tmp/'
CONST_IP_FILE_NAME = 'iplist.info'

CONST_GML_FILE_PATH = '/../gml/'
CONST_GML_FILE_NAME = 'topology.gml'

CONST_USER = 'webadmin'
CONST_PWD = 'webadmin'

CONST_ROOT_PWD = 'root'

CONST_INTERFACES_FILE_PATH = '/etc/network/interfaces'

CONST_NETWORK_BYTE_1 = '10'
CONST_NETWORK_BYTE_2 = '0'
CONST_NETWORK_BYTE_4_1 = '1'
CONST_NETWORK_BYTE_4_2 = '2'

CONST_VLAN_NETMASK = "255.255.255.0"