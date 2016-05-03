# Docker test app

This dir contains a docker test app for agave.

## Things to edit

Two things need to be adjusted to work as your app: in dockerapp/lib/condorSubmit.htc, set the `docker_image` variable to your base image, and the change the `executable` value to your executable or script (which should be run *inside* your image). 

Second, edit the batch\_agavetest.json to have a different id and specify your app's parameters as shown in the [tutorial](../app_tutorial/agaveapps.md). The wrapper.sh script uses some commandline-fu to run a condor-job and poll it until it finishes, which is a workaround as running docker jobs in HTCondor through agave is not supported ATM.

Finally use the batchrunagavetest.json file to run `jobs-submit`. 
