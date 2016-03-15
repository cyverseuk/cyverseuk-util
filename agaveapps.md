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
your client. Next, we'll create login tokens

## Part 2 - System registration (skip if using TGAC hardware)
## Part 3 - App registration
## Part 4 - Discovery Environment
