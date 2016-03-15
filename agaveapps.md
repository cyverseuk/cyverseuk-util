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


## Part 2 - System registration (skip if using TGAC hardware)
## Part 3 - App registration
## Part 4 - Discovery Environment
