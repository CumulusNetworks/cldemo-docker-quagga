Redistributing Docker Bridges into Routing on The Host
======================================================
This demo shows one of several different approaches to running Docker.
This approach advertises entire subnets employed by the docker bridges which are configured on different hosts. In this scenario NAT is not configured anywhere. Using this technique you can provide your containers with real IP addresses which are externally reachable and routed through the Host. 

With Cumulus Quagga installed in a container, as docker bridges are created and destroyed Quagga will see the changes and modify the advertisements into the routed IP fabric.

Using this technique you can deploy containers from a single large 172.16.0.0/16 network.  Each host that may be located in different racks throught the DC owns a /24 subnet from that network and advertises its own subnet into the infrastructure.

### Software in Use:
*On Spines and Leafs:*
  * Cumulus v3.2.0

*On Servers:*
* Ubuntu 16.04
* Docker-CE v17.03
* cumulusnetworks/quagga:latest (container image)
* php:5.6-apache (container image)


Quickstart: Run the demo
------------------------
Before running this demo, install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds) and [Vagrant](https://releases.hashicorp.com/vagrant/). The currently supported versions of VirtualBox and Vagrant can be found in the [cldemo-vagrant](https://github.com/cumulusnetworks/cldemo-vagrant) prequisites section.

```
git clone https://github.com/cumulusnetworks/cldemo-vagrant
cd cldemo-vagrant

vagrant up oob-mgmt-server oob-mgmt-switch
vagrant up leaf01 leaf02 leaf03 leaf04 spine01 spine02 server01 server02 server03 server04

vagrant ssh oob-mgmt-server
sudo su - cumulus

git clone https://github.com/cumulusnetworks/cldemo-roh-docker
cd cldemo-roh-docker

ansible-playbook ./run-demo.yml
```
### Viewing the Results

#### Check on the Cumulus Container
View the configuration of the Quagga routing daemons in the container. Also look at BGP peerings.
```
vagrant ssh oob-mgmt-server
sudo su - cumulus
ssh server01
# Check Configuration
sudo docker exec -it cumulus-roh /usr/bin/vtysh -c "show run"
# Check BGP Peers
sudo docker exec -it cumulus-roh /usr/bin/vtysh -c "show ip bgp sum"
```

#### Test Application Reachability
Here we are using PHP/Apache webservers to represent our container workloads. To test that the applications are reachable across the fabric login to server01 and use the _curl_ command to view an application running on a container across the fabric.
```
vagrant ssh oob-mgmt-server
sudo su - cumulus
ssh server01
curl 172.16.4.1

cumulus@server01:~$ curl 172.16.4.1
<html>
<body>
<h1>HOST: server04 Container ID: 1e473deb7dc6 </h1>
<h1>
Container IPv4 address: 172.16.4.1/24
 </h1>
</body>
</html>
```

## Special Notes

### Privileged Mode Containers
The Cumulus RoH container is deployed as a privileged container with access to the "host" network. This means that the applications running in the container have unfettered access to the interfaces and kernel just like a real baremetal application would. This can be dangerous if the container were to become comprimised as the container essentially has root access.

### Manually Starting and Stopping the Cumulus RoH Container
If you want to try running the Cumulus RoH container in your own environment you can use the automation provided in this repository as a starting point or experiment manually with the container. Notice we're passing in the Quagga.conf file as well to configure the Quagga Routing Daemon upon container startup.

```
# Start the Container
docker run -itd --name=cumulus-roh --privileged --net=host \
    -v /root/quagga/daemons:/etc/quagga/daemons \
    -v /root/quagga/Quagga.conf:/etc/quagga/Quagga.conf \
    cumulusnetworks/quagga:latest

# Stop the Container
docker rm -f cumulus-roh
```

ASCII Demo Topology
-------------------
This demo requires you set up a topology as per the diagram below:

                     +--------------+  +--------------+
                     | spine01      |  | spine02      |
                     |              |  |              |
                     +--------------+  +--------------+
                    swp1-4 ||||                |||| swp1-4
             +---------------------------------+|||
             |             ||||+----------------+|+----------------+
             |             |||+---------------------------------+  |
          +----------------+|+----------------+  |              |  |
    swp51 |  | swp52  swp51 |  | swp52  swp51 |  | swp52  swp51 |  | swp52
    +--------------+  +--------------+  +--------------+  +--------------+
    | leaf01       |  | leaf02       |  | leaf03       |  | leaf04       |
    |              |  |              |  |              |  |              |
    +--------------+  +--------------+  +--------------+  +--------------+
      swp1 |  swp2 \ / swp1 | swp2       swp1 |   swp2 \ / swp1 | swp2
           |        X       |                 |         X       |
      eth1 |  eth2 / \ eth1 | eth2       eth1 |   eth2 / \ eth1 | eth2
    +--------------+  +--------------+  +--------------+  +--------------+
    | server01     |  | server02     |  | server03     |  | server04     |
    |              |  |              |  |              |  |              |
    +--------------+  +--------------+  +--------------+  +--------------+

This topology is also described in the `topology.dot` and `topology.json` files.
Additionally, an out of band management server that can SSH into the leafs and
spines via the specified hostnames is required. Setting up this topology is
outside the scope of this document.

This demo was initially written using Ansible 2.2. Install Ansible on the management server
before you begin. Instructions for installing Ansible can be found here:
https://docs.ansible.com/ansible/intro_installation.html
