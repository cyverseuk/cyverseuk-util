input_str="${input1},${input2},${input3},${input4},${input5},${input6},${input7},${input8}"
param_str="-input1 ${input1} -input2 ${input2} -input3 ${input3} -input4 ${input4} -input5 ${input5} -input6 ${input6} -input7 ${input7} -input8 ${input8}"

if [[ "${refgen}" ]]; then
  input_str="$input_str,${refgen}"
  param_str="$param_str -indx ${refgen}"
fi

if [[ "${refann}" ]]; then
  input_str="$input_str,${refann}"
  param_str="$param_str -gtf ${refann}"
fi

if [[ "${maskfile}" ]]; then
  input_str="$input_str,${maskfile}"
  param_str="$param_str -o ${maskfile}"
fi

if [[ "${maskfilec}" ]]; then
  input_str="$input_str,${maskfilec}"
  param_str="$param_str -E ${maskfilec}"
fi

param_str="$param_str ${lab1} ${lab2} ${lab3} ${lab4} ${indpre} ${fastqscale} ${libtype} ${sensitivity} ${insertsize} ${stdev} ${minanchor} ${minintron} ${maxintron} ${maxalign} ${minreadlength} ${numthreads} ${discalign} ${mixalign} ${usegtf} ${userescue} ${maxit} ${idpre} ${isofrac} ${intraintrtresh} ${maxintronu} ${minintronz} ${junctionalpha} ${anchfrac} ${mintransfrag} ${termexonmax} ${trimcovavg} ${trimfrac} ${transfraggap} ${fragbias} ${userescuecd} ${testalign} ${testfdr} ${normalhits}"

echo transfer_input_files = $input_str >> lib/condorSubmitEdit.htc
echo arguments = \"$param_str\" >> lib/condorSubmitEdit.htc
cat lib/condorSubmit.htc >> lib/condorSubmitEdit.htc

jobid=`condor_submit lib/condorSubmitEdit.htc`
jobid=`echo $jobid | sed -e 's/Sub.*uster //'`
jobid=`echo $jobid | sed -e 's/\.//'`

#echo $jobid

#echo going to monitor job $jobid
condor_tail -f $jobid

exit 0
