Redistributing Docker into Routing on The Host
===============================================
This demo shows one of several different approaches to running Docker.
This approach advertises host-routes for Docker containers which have been created on a docker-bridge without NAT enabled.
Using this technique you can provide your containers with real IP addresses which are externally reachable and routed through the Host. 

Cumulus Quagga is installed in a container along with the CRoHDAd daemon (Cumulus Routing On the Host Docker Advertisement Daemon). The CRoHDAd daemon listens to the docker-engine API and advertises new container IP addresses into the routed BGP fabric as they are created. When containers are destroyed, the daemon also removes the host-routes from the fabric.

Using this technique you can deploy containers from a single large 172.16.0.0/16 subnet owned by multiple docker bridges on different hosts and located in different racks throughout the DC.

### Software in Use:
*On Spines and Leafs:*
  * Cumulus v3.2.0

*On Servers:*
* Ubuntu 16.04
* Docker-CE v17.03
* cumulusnetworks/quagga:crohdad (container image)
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
sudo apt-get install software-properties-common -qy
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update -y
sudo apt-get install ansible python-pip -qy
sudo pip install ansible --upgrade

git clone https://github.com/cumulusnetworks/cldemo-roh-docker
cd cldemo-roh-docker
git checkout crohdad

ansible-playbook ./run-demo.yml
```
### Viewing the Results

#### Watch The CRoHDAd Daemon Advertising Routes
View the output of the CRoHDAd daemon as it is advertising /32 host-routes into the Quagga instance running in the same container.
```
vagrant ssh oob-mgmt-server
sudo su - cumulus
ssh server01
sudo docker logs crohdad

cumulus@server01:~$ sudo docker logs crohdad
Starting Quagga daemons (prio:10):. zebra. bgpd.
Starting Quagga monitor daemon: watchquaggawatchquagga[32]: watchquagga 1.0.0+cl3u9 watching [zebra bgpd], mode [phased zebra restart]
watchquagga[32]: bgpd state -> up : connect succeeded
watchquagga[32]: zebra state -> up : connect succeeded
watchquagga[32]: Watchquagga: Notifying Systemd we are up and running
.
Exiting from the script
RUNNING CROHDAD: /root/crohdad.py -bl &

################################################
#                                              #
#     Cumulus Routing On the Host              #
#       Docker Advertisement Daemon            #
#             --cRoHDAd--                      #
#         originally written by Eric Pulvino   #
#                                              #
################################################

 STARTING UP.
  Auto-Detecting existing containers and adding host routes...
  Listening for Container Activity...


[hit enter key to exit] or run 'docker stop <container>'
STARTED -- Container id: 2ed5afcc86f48e1d7f35b2b940200a77f29e5957d6df743c64b53e38ef13f214
    ADDING Host Route: 172.18.0.1/32 (from container: 2ed5afcc86f4)
STARTED -- Container id: 4937317881fdbb746ec72fd25d1ac469eada8890da2f0c629f30394dfb04250e
    ADDING Host Route: 172.18.0.2/32 (from container: 4937317881fd)
STARTED -- Container id: b2c21cad49beb02289508631d4d64a090c66615a60c1f00f51590a008b150348
    ADDING Host Route: 172.18.0.3/32 (from container: b2c21cad49be)

```

#### Test Application Reachability
Here we are using PHP/Apache webservers to represent our container workloads. To test that the applications are reachable across the fabric login to server01 and use the _curl_ command to view an application running on a container across the fabric.
```
vagrant ssh oob-mgmt-server
sudo su - cumulus
ssh server01
curl 172.21.0.1

cumulus@server01:~$ curl 172.21.0.1
<html>
<body>
<h1>HOST: server04 Container ID: 1e473deb7dc6 </h1>
<h1>
Container IPv4 address: 172.21.0.1/24
 </h1>
</body>
</html>
```

## Special Notes

### Privileged Mode Containers
The CRoHDAd container is deployed as a privileged container with access to the "host" network. This means that the applications running in the container have unfettered access to the interfaces and kernel just like a real baremetal application would. This can be dangerous if the container were to become comprimised as the container essentially has root access.

### Exposing the Docker Unix Socket
The docker CLI is essentially a client that communicates with the Dockerd daemon which runs in the background. That communication happens by default on Linux systems over a Unix Socket which behaves much like a webserver port. When running the CRoHDAd container it is necessary to share this Unix Socket file with the running container so that the docker CLI running inside the container can listen to the docker-engine API to learn about containers and networks as they are reated and destroyed.

### Manually Starting and Stopping the CRoHDAd Container
If you want to try running the CRoHDAd container in your own environment you can use the automation provided in this repository as a starting point or experiment manually with the container. Notice we're passing in the Quagga.conf file as well to configure the Quagga Routing Daemon upon container startup.

```
# Start the Container
docker run -itd --name=crohdad --privileged --net=host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /root/quagga/Quagga.conf:/etc/quagga/Quagga.conf \
    cumulusnetworks/quagga:crohdad

# Stop the Container
docker rm -f crohdad
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

This demo is written using Ansible 2.2. Install Ansible on the management server
before you begin. Instructions for installing Ansible can be found here:
https://docs.ansible.com/ansible/intro_installation.html
