Quagga in Docker
================
This demo shows off two ways of putting Quagga into a Docker container to do
Layer 3 networking on the hosts.

Before you start
----------------
This demo requires you set up a topology as per the diagram below:

             +------------+       +------------+
             | leaf01     |       | leaf02     |
             |            |       |            |
             +------------+       +------------+
             swp1 |    swp2 \   / swp1    | swp2
                  |           X           |
             eth1 |    eth2 /   \ eth1    | eth2
             +------------+       +------------+
             | server01   |       | server02   |
             |            |       |            |
             +------------+       +------------+

This topology is also described in the `topology.dot` and `topology.json` files.
Additionally, an out of band management server that can SSH into the leafs and
spines via the specified hostnames is required. Setting up this topology is
outside the scope of this document.

This demo is written using Ansible 2.0. Install Ansible on the management server
before you begin. Instructions for installing Ansible can be found here:
https://docs.ansible.com/ansible/intro_installation.html

Running the Demo
----------------
On the management server, download the demo and cd into the top directory.
There are two demo playbooks: `demo-docker-vrouter` and
`demo-docker-privileged`. To run them, run the command:
`ansible-playbook <DEMO>.yml -k --ask-sudo-pass`.

After running one demo, you will need to log into the servers and delete the
Docker containers before you can create another one. You can do this with the
command `docker ps -a | docker rm`.

### docker-privileged
Installs Quagga on a privileged Docker container with access to the host
machine's networking stack. In this demo, we set up OSPF-numbered on both
hosts (via Docker) and the leaves, making it possible for one host to ping the
other.

This demo showcases how easy it is to configure Quagga without having to install
the package natively. Since the Cumulus version of Quagga is often ahead of the
official release, it can be packaged into a Docker container without needing to
change the package sources of the host or compile it from source on a non-debian
machine.

### docker-vrouter
This variant of the docker quagga demo leverages Docker and Quagga to create
a lightweight Virtual Router on the server. In this example, we create a
VRouter in order to connect other Docker containers on the host to the Layer 3
fabric, making it possible for a container on server01 to ping a container on
server02 by travelling through docker-router-1, one of the leafs, down through
docker-router-2, and on to its final destination.

The setup is fairly complicated, but the advantage is that this allows a
Docker container to be used as a virtual Cumulus switch, which is slightly more
efficient than a fully virtual solution such as VX.
