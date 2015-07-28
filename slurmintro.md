#SLURM job manager

##Contents
- [Basic stuff](#basic-stuff)
  - [Documentation](#documentation)
  - [Installing](#installing)
- [Basic commands](#basic-commands)
- [slurm.conf](slurmconf)
- [Troubleshooting](troubleshooting)

##Basic stuff

Slurm tutorial vids (playlist): [youtube](https://www.youtube.com/watch?v=NH_Fb7X6Db0&list=PLZfwi0jHMBxB-Bd0u1lTT5r0C3RHUPLj-)

###Documentation:
User quick start: http://slurm.schedmd.com/quickstart.html

Admin quick start: http://slurm.schedmd.com/quickstart_admin.html

man pages for each tool: http://slurm.schedmd.com/man_index.html

###Installing

1. Install MUNGE on all nodes:
  - get tarball from https://github.com/dun/munge
  - unzip/tar and `./configure && make install` *NB. you might need libssl-dev as a dependency*
  - create keyfile `dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key` *Copy the key to all nodes*
  - run the munged daemon: `munged`
2. Install slurm on all nodes:
  - get tarball from http://www.schedmd.com/#repos
  - unzip/tar and `./configure && make install --sysconfdir=/etc/slurm` *NB. You will need automake*
3. Create slurm.conf file:
  - The most barebones slurm.conf would look like this:

    ```
    # /etc/slurm/slurm.conf
    ControlMachine=hostname # Hostname of master controller. On the master itself, this should be the basic hostname as returned by hostname -s
    NodeName=list,of,hosts,supports,brackets[0-99] State=UNKOWN
    PartitionName=partition Nodes=list,of,hosts Default=YES MaxTime=INFINITE State=UP
    ```
  - These three options in the file are the ONLY thing that you need to get slurm up and running.
  - See [slurm.conf](#slurmconf) below for more options
4. Copy slurm.conf to the other nodes in your network
5. Start slurm daemons:
  1. On master: `slurmctld -f /path/to/slurm.conf -Dcvvvv`
  2. On all nodes (including master if you want it to do work): `slurmd -f /path/to/slurm.conf -Dcvvvv`
    - This will run every daemon in the foreground, omit the -D to run in background (see below for full details)
6. Try `sinfo` or `squeue` to see your cluster up and running!

## Basic commands:
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

### sinfo

Shows the status of nodes in the cluster. Useful parameters:
- `-p <partition>` print info from a specific partition
- `-l` print more detailed info
- `-s` print less detailed info

### squeue

Lists the current job queue. Useful parameters:
- `-w <hostlist>` print only the job queue of the specified hosts
- `-u <user>` print jobs from specific user
- `-p <partition>` print jobs from specific partition

quick explanation of status codes:
- **CA** - canceled
- **CD** - completed
- **CG** - completing *See [troubleshooting](#troubleshooting) if jobs are blocking resources with this code*
- **F**  - failed
- **PD** - pending
- **R**  - running
- **S**  - suspended

### srun

The main command to run things in slurm. Important arguments:
- `-n<x>` request this task to be run x amount of times
- `--multi-prog` run with different arguments each task as specified in configuration file:
  - .conf looks like this:
  ```
  # myjob.conf
  0,2-3 coolprog --arg file_default
  # %t is replaced by the task number
  1,3-6 coolprog --arg file%t
  ```
  - run as `srun -n6 --multi-prog myjob.conf`
- `-l` print task number to STDOUT

### scontrol

command to control the state of nodes and the system in general. Use as `scontrol <command>` Useful commands:
-

### scancel

cancel a job. Use as `scancel <jobid>`

##slurm.conf

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

http://slurm.schedmd.com/slurm.conf.html or `man slurm.conf`

##Troubleshooting

If your jobs are hanging in a completing state ('CG' in squeue), run:

`scontrol update NodeName=<node> State=down Reason=hung_proc && scontrol update NodeName=<node> State=resume`

This resets all jobs, so be careful. For details see here: http://slurm.schedmd.com/troubleshoot.html#completing
