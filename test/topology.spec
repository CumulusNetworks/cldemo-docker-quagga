  
vm oob-mgmt-server ubuntu-16.04 2 4 10 
vm leaf01 cumulus-vx-3.2.1 1 2 10 
vm leaf02 cumulus-vx-3.2.1 1 2 10 
vm leaf03 cumulus-vx-3.2.1 1 2 10 
vm leaf04 cumulus-vx-3.2.1 1 2 10 
vm spine01 cumulus-vx-3.2.1 1 2 10 
vm spine02 cumulus-vx-3.2.1 1 2 10 
vm server01 ubuntu-16.04 2 4 10 
vm server02 ubuntu-16.04 2 4 10 
vm server03 ubuntu-16.04 2 4 10 
vm server04 ubuntu-16.04 2 4 10 
 
network oob-mgmt-server eth0 10.255.0.1 255.255.0.0 public 
service oob-mgmt-server ssh 10.255.0.1 22 TCP public 
service oob-mgmt-server http 10.255.0.1 80 TCP public 
service oob-mgmt-server https 10.255.0.1 443 TCP public 
service oob-mgmt-server novnc 10.255.0.1 6080 TCP public 
 
network oob-mgmt-server eth1 192.168.0.254 255.255.0.0 
network leaf01 eth0 192.168.0.11 255.255.0.0 
network leaf02 eth0 192.168.0.12 255.255.0.0 
network leaf03 eth0 192.168.0.13 255.255.0.0 
network leaf04 eth0 192.168.0.14 255.255.0.0 
network spine01 eth0 192.168.0.21 255.255.0.0 
network spine02 eth0 192.168.0.22 255.255.0.0 
network server01 eth0 192.168.0.31 255.255.0.0 
network server02 eth0 192.168.0.32 255.255.0.0 
network server03 eth0 192.168.0.33 255.255.0.0 
network server04 eth0 192.168.0.34 255.255.0.0 
 
autoconfig oob-mgmt-server 
 
 connect leaf01 swp51 spine01 swp1 
 connect leaf02 swp51 spine01 swp2 
 connect leaf03 swp51 spine01 swp3 
 connect leaf04 swp51 spine01 swp4 
 connect leaf01 swp52 spine02 swp1 
 connect leaf02 swp52 spine02 swp2 
 connect leaf03 swp52 spine02 swp3 
 connect leaf04 swp52 spine02 swp4 
 connect leaf01 swp49 leaf02 swp49 
 connect leaf01 swp50 leaf02 swp50 
 connect leaf03 swp49 leaf04 swp49 
 connect leaf03 swp50 leaf04 swp50 
 connect spine01 swp31 spine02 swp31 
 connect spine01 swp32 spine02 swp32 
 connect server01 eth1 leaf01 swp1 
 connect server01 eth2 leaf02 swp1 
 connect server02 eth1 leaf01 swp2 
 connect server02 eth2 leaf02 swp2 
 connect server03 eth1 leaf03 swp1 
 connect server03 eth2 leaf04 swp1 
 connect server04 eth1 leaf03 swp2 
 connect server04 eth2 leaf04 swp2 
 connect leaf01 swp45 leaf01 swp46 
 connect leaf01 swp47 leaf01 swp48 
 connect leaf02 swp45 leaf02 swp46 
 connect leaf02 swp47 leaf02 swp48 
 connect leaf03 swp45 leaf03 swp46 
 connect leaf03 swp47 leaf03 swp48 
 connect leaf04 swp45 leaf04 swp46 
 connect leaf04 swp47 leaf04 swp48 
