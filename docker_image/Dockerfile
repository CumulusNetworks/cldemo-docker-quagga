FROM ubuntu:14.04
MAINTAINER Barry Peddycord III <bwpeddyc@cumulusnetworks.com>

COPY debs/* /root/
RUN apt-get install iptables iproute -y
RUN dpkg -i /root/quagga_0.99.23.1-1+cl2.5_amd64.deb
RUN dpkg -i /root/quagga-dbg_0.99.23.1-1+cl2.5_amd64.deb
RUN dpkg -i /root/quagga-doc_0.99.23.1-1+cl2.5_all.deb
RUN apt-get install -f
COPY quagga/quagga_daemon /etc/quagga/daemons

ENTRYPOINT ["/bin/bash"]
