Quagga in Docker
================
This demo shows off two ways of putting Quagga into a Docker container to do
Layer 3 networking on the hosts.



Quickstart: Run the demo
------------------------
(This assumes you are running Ansible 1.9.4 and Vagrant 1.8.4 on your host.)

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    git checkout 2.5.x
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02 leaf03 leaf04 spine01 spine02 server01 server02 server03 server04
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    sudo apt-get install software-properties-common -qy
    sudo apt-add-repository ppa:ansible/ansible -y
    sudo apt-get update
    sudo apt-get install ansible -qy
    git clone https://github.com/cumulusnetworks/cldemo-docker-quagga
    cd cldemo-docker-quagga
    git checkout 2.5.x
    ansible-playbook run-demo.yml
    ssh server01
    wget 10.0.0.32
    cat index.html


Before you start
----------------
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

This demo is written using Ansible 2.0. Install Ansible on the management server
before you begin. Instructions for installing Ansible can be found here:
https://docs.ansible.com/ansible/intro_installation.html

Running the Demo
----------------
On the management server, download the demo and cd into the top directory.
Run the command: `ansible-playbook run-demo.yml`.

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
