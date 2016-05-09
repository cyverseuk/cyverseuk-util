echo "#!/bin/bash" >> blastedit.sh
echo QUERY="${query}" >> blastedit.sh
echo DATABASE="${database}" >> blastedit.sh
cat lib/blast.sh >> blastedit.sh

echo transfer_input_files = lib/makeblastdb,lib/blastn,${query},${database} >> lib/condorSubmitEdit.htc
cat lib/condorSubmit.htc >> lib/condorSubmitEdit.htc


jobid=`condor_submit lib/condorSubmitEdit.htc`
jobid=`echo $jobid | sed -e 's/Sub.*uster //'`
jobid=`echo $jobid | sed -e 's/\.//'`

#echo $jobid

#echo going to monitor job $jobid
condor_tail -f $jobid

exit 0
