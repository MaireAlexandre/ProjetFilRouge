su

#téléchargement du paquet serveur DHCP
apt-get install isc-dhcp-server

#configuration de l'interface réseau éthernet eth0
nano /etc/network/interfaces

#redémarrage de l'interface eth0 pour appliquer la configuration
ifdown eth0
ifup eth0

#configuration du serveur dhcp CF conf2
cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.old
nano /etc/dhcp/dhcpd.conf

#redémarrage du service dhcp
service isc-dhcp-server restart

#conf1
ajouter dans le fichier /etc/network/interfaces pour l'interface souhaitée
auto ethX
iface ethX inet static
network 10.0.0.0
address 10.0.0.2
netmask 255.255.255.0

#si le dhcp doit être actif sur une interface spécifique
ajouter dans /etc/default/isc-dhcp-server
INTERFACES="ethX"

#conf2
ajouter dans le fichier /etc/dhcp/dhcpd.conf
subnet 10.0.0.0 netmask 255.255.255.0 {
	range 10.0.0.10 10.0.0.29;
	option broadcast-address 10.0.0.30;
	option routers 10.0.0.2;
	default-lease-time 600;
	max-lease-time 7200;
}
