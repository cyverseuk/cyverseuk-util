# Adding HPC workflows to Agave (Tutorial)

This tutorial is based on Sam Mason's tutorial, and updated and adjusted 
slightly for TGAC hardware.

## Overview
In this tutorial, you'll set up a simple app that runs through the Agave API 
on the TGAC HTCondor cluster or your own hardware. The only preliminary is 
a CyVerse account, for which you can sign up 
[here](http://user.iplantcollaborative.org/) (don't worry, it's free). You'll
also need to have git installed on the machine you will be working on. Let's 
get going!
## Part 1 - Setting up Agave API Access
First, you'll need to configure your environment to have API access. The easiest
way is to download the Agave-CLI package: 

`git clone https://bitbucket.org/taccaci/foundation-cli`

This will create a 
`foundation-cli` directory in your current directory. To shorten our commands,
let's add it to our PATH: 

``export PATH=$PATH:`pwd`/foundation-cli/bin`` 

Now that we can access the API commands, let's set up the keys to allow API 
access. You'll need to specify a tenant, wich is probably going to be 
`iplantc.org`, which at the time of writing is option 3:

```bash
vandene@n80295:~$ tenants-init
Please select a tenant from the following list:
[0] agave.prod
[1] araport.org
[2] designsafe
[3] iplantc.org
[4] irec
[5] irmacs
[6] tacc.prod
[7] vdjserver.org
[8] wso2.agave.staging
[9] xsede.org
[10] xsede.org.staging
Your choice [3]: 3
You are now configured to interact with the APIs at https://agave.iplantc.org/
vandene@n80295:~$
```

Then create a new client:

`clients-create -N cli_client -u username -S`

You'll be asked for your password and a message will confirm the creation of 
your client. Next, we'll create login tokens:

`auth-tokens-create -S`

You'll be asked for your password once more, and a message will confirm creation
of your tokens. Should your tokens ever expire during your session, run the 
refresh command:

`auth-tokens-refresh -S`

Now that we have our credentials set up, we can start actually registering and 
using apps. The next section deals with registering your own system; it can be
skipped if you are using TGAC hardware. All examples here are given using TGAC
systems.
## Part 2 - System registration (skip if using TGAC hardware)
Agave is a RESTful API, meaning that we can interact with it using POST and GET
http requests. The foundation-cli tools are essentially wrappers around these 
types of requests to make these requests shorter.

Agave tracks two kinds of resources: Systems and Apps. There are 2 types of
Systems: Storage and Execution. Apps run on Execution Systems using data from
Storage Systems to produce desired results. So to run an app, we need an 
Execution system first. Systems are described using JSON files, which are then
posted to the API. An Execution System JSON consists of 4 parts, which will be
described below.
### Execution System JSON - System Basics
The first part consists of system basics: id, type etc. See an example below:

```
"id"            : "myTutorialMachine",
"name"          : "A machine for the TGAC Agave tutorial",
"type"          : "EXECUTION",
"executionType" : "CLI",
"scheduler"     : "FORK",
```

The variables mostly speak for themselves. The `executionType` variable can be
either CLI, CONDOR or HPC depending on the type of scheduler running on the
system. In this case, we assume there is no scheduler running and so we choose
`CLI`, with `FORK` as a scheduler. See [the Agave docs](http://agaveapi.co/documentation/tutorials/system-management-tutorial/#execution-systems)
for more details on the Scheduler variables.
### Execution System JSON - Storage
All Execution systems need a Storage system from which they will draw data.
Assuming your data lives on the CyVerse servers, we'll use that datastore for 
this example. 

```
"storage": {
  "host" : "data.iplantcollaborative.org",
  "port" : 1247,
  "protocol" : "IRODS",
  "homedir" : "/iplant/home/username",
  "rootdir" : "/iplant/home",
  "auth" : {
    "type": "PASSWORD",
    "username": "username",
    "password": "changethis"
  },
  "zone" : "iplant",
  "resource" : "bitol"
}
```

Remember to change your username and password in the above example! Obviously,
if you are using an alternative storage system, you'll need to change those 
variables as well. A simple example using your own machine and SFTP as a transfer
mechanism would be as follows:

```
"storage": {                                                                    
  "host" : "yourhost.example.org",                                      
  "port" : 22,                                                                
  "protocol" : "SFTP",                                                         
  "auth" : {                                                                    
    "type": "PASSWORD",                                                         
    "username": "username",                                                     
    "password": "changethis"                                                    
  },                                                                            
}     
```

Putting your password in plaintext is usually a bad idea, so see below for setting
up alternative login methods using public/private keypairs.
### Execution System JSON - Queues
All execution systems need a default Queue to which jobs are submitted. In our
example, we are using a simple CLI system, so there are no scheduler queues that
we need to deal with. This means we can get away with a simple specification like
this:

```
"queues": [ { 
    "name": "normal", 
    "default": true,
    "maxRequestedTime": "24:00:00",
    "maxJobs": 10, 
    "maxUserJobs": 5, 
    "maxNodes": 1,
    "maxMemoryPerNode": "4GB", 
    "maxProcessorsPerNode": 12,
    "customDirectives": null 
} ]
```

You'll want to change the variables to suit your system.
### Execution System JSON - Login
Lastly, Agave will need to know information to login to the Execution system. 
This can be specified using a Login object, which is specified as follows:

```
"login": {
  "host"    : "149.155.193.71",
  "port"    : "22",
  "protocol": "SSH",
  "auth"    : {
    "type"      : "PASSWORD",
    "username"  : "username",
    "password"  : "changethis"
  }
}
```

Like mentioned before, posting your password in plaintext is usually a bad idea.
We can specify a login object using public and private keys as well. To do this
we'll change the `auth` part of the object as follows:
```
"auth" {
  "type"       : "SSHKEYS",
  "username"   : "username",
  "publicKey"  : "ssh-rsa AAAA...your public key... username@yourhost.example.org",
  "privateKey" : "-----BEGIN RSA PRIVATE KEY-----*private key here*-----END RSA PRIVATE KEY-----"
}
```

An important thing to note when using keypairs is that your private key should
be JSON encoded before pasting it into the JSON file using the `jsonpki` command:

`json-pki --private /path/to/private/id_rsa`

A password for the file can be specified using `--password`. 

## Part 3 - App registration
## Part 4 - Discovery Environment
