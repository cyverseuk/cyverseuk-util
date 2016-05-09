echo transfer_input_files = ${input1},${input2},${input3},${input4},${input5},${input6},${input7},${input8},${refgen},${refann},${maskfile},${maskfilec} >> lib/condorSubmitEdit.htc
echo arguments = ${lab1},${lab2},${lab3},${lab4},${indpre},${fastqscale},${libtype},${sensitivity},${insertsize},${stdev},${minanchor},${minintron},${maxintron},${maxalign},${minreadlength},${numthreads},${discalign},${mixalign},${usegtf},${userescue},${maxit},${idpre},${isofrac},${intraintrtresh},${maxintron},${minintron},${maxintron},${maxalign},${minreadlength},${numthreads},${discalign},${mixalign},${usegtf},${userescue},${maxit},${idpre},${isofrac},${intraintrtresh},${maxintron},${minintron},${junctionalpha},${anchfrac},${mintransfrag},${termexonmax},${trimcovavg},${trimfrac},${transfraggap},${transfraggap},${userescuecd},${testalign},${testfdr},${normalhits} >> lib/condorSubmitEdit.htc
cat lib/condorSubmit.htc >> lib/condorSubmitEdit.htc

jobid=`condor_submit lib/condorSubmitEdit.htc`
jobid=`echo $jobid | sed -e 's/Sub.*uster //'`
jobid=`echo $jobid | sed -e 's/\.//'`

#echo $jobid

#echo going to monitor job $jobid
condor_tail -f $jobid

exit 0
