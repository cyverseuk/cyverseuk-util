#!/bin/bash

for node in `cat /home/admin/loadavg/nodes`
do
  slotname=slot1@$node
  loadavg=$(condor_status -l $slotname | grep TotalLoadAvg | sed 's/TotalLoadAvg = //')
  #echo [`date`] Reporting load of $loadavg for machine $node >> /home/admin/loadavg/loadavg.log
  response=$(curl -s --data "action=report_load" --data "machine=$node" --data "load=$loadavg" "54.76.233.126/api.php?")
  #echo [`date`] Got \"$response\" from server >> /home/admin/loadavg/loadavg.log
done
