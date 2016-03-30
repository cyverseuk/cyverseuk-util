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

```json
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

```json
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

```json
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

```json
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

```json
"login": {
  "host"    : "yourhost.example.org",
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
```json
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

### Registering the execution system

Now that we have a [completed JSON file](TutSystem.json), let's use it to register the system on 
Agave:

`vandene@n80295:~$ systems-addupdate -v -F TutSystem.json`

A large amount of JSON describing our new system will be returned to confirm the
registration. Now that we have an execution system, let's move on to registering
our workflow as an App in the next part.
## Part 3 - App registration
An App in the Agave API means a workflow that is wrapped into a single unit which 
can be executed by a user. It is described in the same way a system is described: JSON.
In this part we'll register a test app that runs a simple BLAST job.

### App JSON - Front matter
The first thing we'll need to describe are some basic parameters of our app:

```json
"name"          : "blastapp-tutorial",
"label"         : "TGAC tutorial BLAST app",
"version"       : "0.0.1",
"executionType" : "CLI",
```

It is important to note that our App's id will be generated from the name and the version number
and that this combination *must be unique*. That means that if we make an update to our app and
try and register it again, we must increment the version number to create a new unique identifier.

Next, we'll specify where and how the app will run:

```json
"executionSystem"  : "myhost.example.org",
"deploymentPath"   : "username/apps/tgac_tutorial",
"templatePath"     : "wrapper.sh",
"testPath"         : "test.sh",
"parallelism"      : "SERIAL",
```

When specifying an `executionSystem` only like above, *you must make sure your app assets are
already present on the system!*. This means that you need admin access to your execution system.
Often this is not the case. To remedy this, we can store our apps assets on the CyVerse Datastore
and specify a "deploymentSystem" parameter like so:

`"deploymentSystem" : "data.iplantcollaborative.org",`

Now that we have specified this, we'll have to actually upload our app's assets to CyVerse.

### Storing App assets with CyVerse

We'll upload data to the datastore using the Discovery Environment (DE), however, the CyVerse datastore uses iRods under
the hood, so you could use [icommands](https://docs.irods.org/master/icommands/user/) as well. For 
more details, see the [CyVerse wiki](https://pods.iplantcollaborative.org/wiki/display/DS/Using+iCommands).

First, login to the DE at [https://de.iplantcollaborative.org/]. You'll be presented with a desktop
like environment. Click on the "Data" button. This will open up a file manager window, with a file
tree on the left hand side. Here, click on the folder with your username (at the top). We'll create
a new folder to hold our apps first. Go to "File" and select "New Folder...". Name the new folder
"TGAC_tutorial" and click "OK" to confirm. Navigate to our newly created folder by clicking on it.
This is where our app's assets will live, which we'll create in the next sections.

### Creating the App assets

For our minimal BLAST app, we'll need three files: a wrapper script, a test script and an executable.
Because of the way BLAST works, we'll actually need two executables for this app. First we'll create
the wrapper script:

```bash
#!/bin/bash

QUERY="${query}"
DATABASE="${database}"

lib/./makeblastdb -dbtype nucl -in $DATABASE -out db
lib/./blastn -query $QUERY -db db

return $!;
```

As you can see from the first line, this is a plain bash script that runs our pipeline. The
next two lines set up our main two parameters: the query and the database. The `${query}`
directive will be replaced BEFORE execution of the script by Agave to the inputs we have given.
Note that the word query is the id we specified in our JSON file earlier. The next line
does the same for the database file.

The next two lines run our actual BLAST 'pipeline': first we create our database with makeblastdb
and we then execute the BLAST with blastn. The `lib/` part of the commandline is because of 
the way we will set up our app assets; Agave convention requires that all our App's executables
are stored in a separate lib directory. We output the database in the first line with a simple 
title of db, and we call that database again in the next line.

The last line returns the current exit status, which will be inherited from the status of BLAST;
this means that the script will pass on BLAST's exit value as its own.

Next, we'll need a test script that test our app with some default data. This is useful, but we'll
skip this for now as it is a bit out of this tutorials' scope. Instead, we'll just write a script
that returns true and call it done:

```bash
#!/bin/bash

return true
```

Finally we'll need to provide the BLAST executables. These can be obtained from the [NCBI ftp server](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
but they are included in this repo to make things easy:

[makeblastdb](lib/makeblastdb)
[blastn](lib/blastn)

Now that we have everything, let's get our assets setup in the datastore. Go back to your DE window,
and go the the tgac_tutorial folder under your username (if you weren't already there). Create a folder
called lib, and navigate to it. We'll put our BLAST executables here. Go to the "Upload" menu on the 
top left-hand corner of the file navigation window. The easiest way is to upload the executables from
this repo directly, so choose "Import from URL...". In the dialog that pops up, put the addresses of
the executables in two separate fields:

`https://github.com/erikvdbergh/cyverseuk-util/raw/master/lib/blastn`

`https://github.com/erikvdbergh/cyverseuk-util/raw/master/lib/makeblastdb`

Notifications will pop up informing you that the upload has started. After a few minutes, refresh the directory
with the "Refresh" button at the top of the file manager window and both files should appear. Using
the file tree, navigate back to the parent "tgac_tutorial" directory. We will upload our wrapper and test
scripts here. Again, go to the "Upload" menu, but choose the "Simple Upload from Desktop" option.
Using the "Browse..." button, navigate to your "wrapper.sh" script and open it. Do the same in the
next field for your "test.sh" script, and click "Upload". After receiving a notification that the 
upload was successful, refresh youor directory again. You should now see our test.sh and wrapper.sh
scripts in the folder, together with the lib directory.

### Registering App in Agave
Now that our assets are in place, we can register our app in Agave using the JSON file we wrote earlier
(If needed, refresh your access tokens with `auth-tokens-refresh`).
Navigate to where the file is stored (we'll assume you've named it TutApp.json) and run the apps-addupdate command:

`apps-addupdate -v -F TutApp.json`

A bunch of JSON describing your app will be returned, confirming the registration of our app.

### Running our App

Finally, we can run our App! We'll need one more (short) JSON file to run a new job:

```json
{
  "name"    : "blasttest",
  "appId"   : "blastapp-tutorial-0.0.1",
  "archive" : "true",
  "inputs": {
    "query"   : "https://github.com/erikvdbergh/cyverseuk-util/raw/master/testquery.fa",
    "database": "https://github.com/erikvdbergh/cyverseuk-util/raw/master/testdb.fa"
  }
}
```

We'll save this file as RunApp.json and submit it as a job with the jobs-submit command:

`jobs-submit -v -W -F RunApp.json`

The -W flag in this command tells it to keep watching the job in the current window, with can be stopped with Ctrl-C.

After your job has completed, your outputs, logs and error messages will be in a folder that is
generated automatically on your apps storage system (which is the CyVerse data store in our case).
To view them on the CyVerse data store, check the "archive" folder under your username. All your
job output will be in a separate subfolder under the "jobs" folder.
## Part 4 - Discovery Environment
