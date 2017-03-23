ansible-playbook run-demo.yml
ssh server01 wget -T 30 -t 1 172.16.4.1
ssh server01 cat index.html
