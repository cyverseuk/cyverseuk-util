This directory contains files that are essential for HTCondor node deployment. 

Step by step guide for deploying a node:
* Set-up apt-get proxy and external source repos - [/etc/apt/sources.list.d/trusty.list](trusty.list)
* install docker - `sudo apt-get install docker-engine`
* install HTCondor - `sudo apt-get install condor`
* add iptables rule - `sudo iptables -I INPUT 36 -p tcp -s 10.0.72.0/24 --dport 5000:6000 -j ACCEPT`
* add condor user to docker group - `gpasswd -a condor docker`
* get [/etc/condor/condor_config](node_config)
* copy and load docker images (see here) - images installed are debian, ubuntu, ubuntu:wily, ubuntu:trusty, ubuntu:precise
* start htcondor - `sudo service condor start`
* run `condor_status` to see if your node pops up
