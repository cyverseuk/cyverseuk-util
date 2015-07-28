#SLURM job manager
##Basic stuff

Slurm tutorial vids (playlist): https://www.youtube.com/watch?v=NH_Fb7X6Db0&list=PLZfwi0jHMBxB-Bd0u1lTT5r0C3RHUPLj-

###Documentation:
User quick start: http://slurm.schedmd.com/quickstart.html

Admin quick start: http://slurm.schedmd.com/quickstart_admin.html

man pages for each tool: http://slurm.schedmd.com/man_index.html

###Installing

1. Install MUNGE on all nodes
  - Get tarball from https://github.com/dun/munge
  - unzip/tar and `./configure && make install` *NB. you might need libssl-dev as a dependency*
  - create keyfile `dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key` *Copy the key to all nodes*
  - run the munged daemon `munged`
2. Install slurm
  - Get tarball from http://www.schedmd.com/#repos
  - unzip/tar and `./configure && make install --sysconfdir=/etc/slurm` *NB. you will need to have automake installed*
  - Create a slurm.conf file (see below for values) and put it in /etc/slurm
  - (On master) run slurmctld
  - (On all nodes) run slurmd
3. Create slurm.conf file
```
# /etc/slurm/slurm.conf
ControlMachine=hostname #Hostname of master controller. On the master itself, this should be the basic hostname as returned by hostname -s
NodeName=comma,separated,list,of,hosts,supports,brackets[0-99] State=UNKOWN
PartitionName=partition Nodes=list,of,hosts,in,this,partition Default=YES MaxTime=INFINITE State=UP
```
These three options in the file are the ONLY thing that you need to get slurm up and running.
Copy slurm.conf to the other machines in your network.

4. Start slurm daemons:
  1. On master: `slurmctld -f /path/to/slurm.conf -Dcvvvv`
  2. On all nodes (including master if you want it to do work): `slurmd -f /path/to/slurm.conf -Dcvvvv`

This will run every daemon in the foreground, omit the -D to run in background (see below for full details)

5. Try `sinfo` or `squeue` to see your cluster up and running!

### Basic commands:
### slurmctld
- Run on master only
- First run: try `slurmctld -Dcvvvv`
  - `-D` run in foreground (dont daemonize)
  - `-c` clear queue, jobs and state ("clean slate")
  - `-v` verbose, each v increases verbosity *EG -vvvv is very verbose*
- Other options:
  - `-L logfile` write messages to this file, using verboseness given by `-v` *Also see SlurmctldLogFile option below*

### slurmd
- Run on every compute node
- First run: try `slurmd -Dcvvvv`
  - `-D` run in foreground (dont daemonize)
  - `-c` clear queue, jobs and state ("clean slate")
  - `-v` verbose, each v increases verbosity *EG -vvvv is very verbose*
- Other options:
  - `-L logfile` write messages to this file, using verboseness given by `-v` *Also see SlurmdLogFile option below*

###slurm.conf

To reload SLURM configuration run `scontrol reconfigure`. This will reconfigure all daemons on all nodes.

####Location of slurm.conf
- If you compiled and installed slurm, location of slurm.conf defaults to ???, but can be given in the configure step, e.g `./configure --sysconfdir=/path/to/dir`
- On Ubuntu/Debian systems: TBA
- Redhat/CentOS: TBA

####Essential options:

- **ControlMachine**=*hostname* - Hostname of master controller *NB on the master itself, this should be the basic hostname as returned by hostname -s*
- **NodeName**=comma,separated,list,of,hosts,supports,brackets[0-99] State=UNKOWN
- **PartitionName**=partition Nodes=list,of,hosts,in,this,partition Default=YES MaxTime=INFINITE State=UP


####Additional options that can be handy:

**Epilog**=/path/to/script - script that is executed after every job

**RebootProgram**=reboot_prg - command that should be executed to reboot a node through the "scontrol reboot_nodes" command

**SlurmUser**=*user* - user that slurmctld runs as, defaults to root but should be slurm or something similar

**SlurmdUser**=*user* - user that slurmd runs as, defaults to root but should be slurm or something similar

**SlurmctldDebug**=*level* - verboseness of slurmctld logging. Default is info, which is not very verbose; for debugging try 'debug5'. Dont forget to set the log location with `slurmctld -L` or the SlurmctldLogFile option (see below)

**SlurmctldLogFile**=/path/to/file - the location of the log for the slurmctld

**SlurmdDebug**=*level* - verboseness of slurmd logging. Default is info, which is not very verbose; for debugging try 'debug5'. Dont forget to set the log location with `slurmd -L` or the SlurmdLogFile option (see below)

**SlurmdLogFile**=/path/to/file - the location of the log for the slurmd


#####Full list of options can be found here:

http://slurm.schedmd.com/slurm.conf.html

###Troubleshooting

If your jobs are hanging in a completing state ('CG' in squeue), run:

`scontrol update NodeName=<node> State=down Reason=hung_proc && scontrol update NodeName=<node> State=resume`

This resets all jobs, so be careful. For details see here: http://slurm.schedmd.com/troubleshoot.html#completing
