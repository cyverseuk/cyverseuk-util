#SLURM job manager
##Basic stuff

Slurm starting with: https://www.youtube.com/watch?v=NH_Fb7X6Db0&list=PLZfwi0jHMBxB-Bd0u1lTT5r0C3RHUPLj-

###Documentation:
User quick start: http://slurm.schedmd.com/quickstart.html

Admin quick start: http://slurm.schedmd.com/quickstart_admin.html

man pages for each tool: http://slurm.schedmd.com/man_index.html

###Installing

1. Install MUNGE on all nodes
  - Get tarball from https://github.com/dun/munge
  - unzip/tar and `./configure && make install` *NB you might need libssl-dev as a dependency*
  - create keyfile `dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key` *Copy the key to all nodes*
  - run the munged daemon `munged`
2. Install slurm
  - Get tarball from http://www.schedmd.com/#repos
  - unzip/tar and `./configure && make install --sysconfdir=/etc/slurm` *NB you will need to have automake installed*
  - Create a slurm.conf file (see below for values) and put it in /etc/slurm
  - (On master) run slurmctld
  - (On all nodes) run slurmd

### Basic commands:
### slurmctld
- Run on master only
- First run: try `slurmctld -Dcvvvv`
  - `-D` run in foreground (dont daemonize)
  - `-c` clear queue, jobs and state ("clean slate")
  - `-v` verbose, each -v increases verbosity

### slurmd
- Run on every compute node
- First run: try `slurmd -Dcvvvv`
  - `-D` run in foreground (dont daemonize)
  - `-c` clear queue, jobs and state ("clean slate")
  - `-v` verbose, each -v increases verbosity

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

These three options in the file are the ONLY thing that you need to get slurm up and running:

1. Copy slurm.conf to the other machines in your network
2. Start slurmctld on your master
3. Start the slurmd on all nodes (including master if you want it to perform work)

Additional options that can be handy:

Full list of options can be found here:
