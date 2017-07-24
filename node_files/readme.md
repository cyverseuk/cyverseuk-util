This directory contains files that are essential for HTCondor node deployment. 

### Ubuntu

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

### Centos

Step by step guide to deploy a submit node:
* Install the htcondor repositories: 
  ```
  cd /etc/yum.repos.d  
  wget https://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo
  ``` 
  (change this accordingly to the version - see https://research.cs.wisc.edu/htcondor/yum/)
* Import key, for centos 6 and 7: 
  ```
  wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor  
  rpm --import RPM-GPG-KEY-HTCondor
  ```
* install condor: `yum install condor.x86_64`
* change the `/etc/condor/condor_config` file as in [example](centos_submit)
* start the daemons: `systemctl start condor.service`
* check everything is working OK:
  * `ps -aux | grep condor_` should show condor_master, condor_shared_port and condor_schedd_running.
  * condor_q, condor_status return correctly
  * the manager node can see the new submit node in the pool (`condor_status --schedd`)
