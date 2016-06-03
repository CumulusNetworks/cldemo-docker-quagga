FROM ubuntu:16.04
MAINTAINER Barry Peddycord III <bwpeddyc@cumulusnetworks.com>

COPY quagga_0.99.23.1-1+cl3u2_xenial_amd64.deb /root/
COPY quagga-dbg_0.99.23.1-1+cl3u2_xenial_amd64.deb /root/
COPY quagga-doc_0.99.23.1-1+cl3u2_xenial_all.deb /root/
RUN apt-get update
RUN apt-get install iptables iproute libjson-c2 -y
RUN dpkg -i /root/quagga_0.99.23.1-1+cl3u2_xenial_amd64.deb
RUN dpkg -i /root/quagga-dbg_0.99.23.1-1+cl3u2_xenial_amd64.deb
RUN dpkg -i /root/quagga-doc_0.99.23.1-1+cl3u2_xenial_all.deb
RUN apt-get install -f
COPY daemons /etc/quagga/daemons

ENTRYPOINT ["/bin/bash"]
