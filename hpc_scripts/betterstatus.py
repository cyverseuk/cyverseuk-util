from __future__ import print_function
import htcondor
import time

def deltatime( pit ):
    now = int(round(time.time()))
    time_up = now - pit

    days_up = time_up // (24 * 60 * 60)
    time_up -= days_up * (24 * 60 * 60)

    hours_up = time_up // (60 * 60)
    time_up -= hours_up * (60 * 60)

    mins_up = time_up // 60
    time_up -= mins_up * 60

    return str(days_up)+"+"+'{:02d}'.format(hours_up)+":"+'{:02d}'.format(mins_up)+":"+'{:02d}'.format(time_up)

coll = htcondor.Collector("10.0.72.17:4080?sock=collector")
slots = coll.query();

print("########")
print("#Status#")
print("########")

#for slot in slots:
#    slottype = slot.get("SlotType", "none")
#    if slottype == "Partitionable":
#        print(slot["Name"],"\t\t\t",slot["DetectedCpus"],"\t",slot["TotalMemory"])
#        for i in range (0, len(slot["ChildName"])):
#          print("\t",slot["ChildName"][i],"\t",slot["ChildCpus"][i],"\t",slot["ChildMemory"][i],slot["ChildEnteredCurrentState"][i])

slotindex = 0;

out = []

for slot in slots:
    slottype = slot.get("SlotType", "none")
    if slottype == "Partitionable":
        parentslot = slotindex
        out.append([])
        out[slotindex].append(0) #indicate if child
        out[slotindex].append(slot["Name"])
        out[slotindex].append(slot["Activity"])
        out[slotindex].append(0) #placeholder for cpus in use
        out[slotindex].append(slot["DetectedCpus"])
        out[slotindex].append(0) #placeholder for mem in use
        out[slotindex].append(slot["TotalMemory"])
        out[slotindex].append(deltatime(slot["EnteredCurrentActivity"]))
        slotindex += 1

        for i in range (0, len(slot["ChildName"])):
            out.append([])
            out[slotindex].append(1) #indicate if child
            out[slotindex].append(slot["ChildName"][i])
            out[slotindex].append(slot["ChildActivity"][i])
            out[slotindex].append(slot["ChildCpus"][i])
            out[slotindex].append(0)
            out[slotindex].append(slot["ChildMemory"][i])
            out[slotindex].append(0)

            out[slotindex].append(deltatime(slot["ChildEnteredCurrentState"][i]))

	    out[parentslot][3] += out[slotindex][3]
	    out[parentslot][5] += out[slotindex][5]

	    slotindex += 1

print("name\tactivity\tcpus_used\tmem_used\tuptime")
for i in range (0, len(out)):
    for j in range (5,7):
        if out[i][j] > 1000 or out[i][j] == 0:
            out[i][j] = out[i][j] // 1000
            out[i][j] = str(out[i][j])+"G"
        else:
            out[i][j] = round(out[i][j] / 1000.0, 2)
            out[i][j] = str(out[i][j])+"G"
    if out[i][0] == 1:
        #print the tree graphic
        if i == len(out)-1 and out[i][0] == 1:
            print(u'\u2514'.encode('utf-8'),end="")
        elif out[i+1][0] == 1:
            print(u'\u251C'.encode('utf-8'),end="")
        else:
            print(u'\u2514'.encode('utf-8'),end="")
	out[i][4] = '';
	out[i][6] = '';
    else:
        out[i][3] = str(out[i][3])+"/"+str(out[i][4])
	out[i][4] = '';

        out[i][5] = str(out[i][5])+"/"+str(out[i][6])
	out[i][6] = '';
    for j in range (1, len(out[i])):
        print(out[i][j],"\t",end="")
    print('')
        
schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd, "localhost")
schedd = htcondor.Schedd(schedd_ad)
jobs = schedd.query();

print("#######")
print("#Queue#")
print("#######")

statuses = {
    1: 'Idle',
    2: 'Running',
    3: 'Removed',
    4: 'Completed',
    5: 'Held',
    6: 'Submission Error'
}

print("jobid\tstate\tcmd\tdocker_img\truntime")
for job in jobs:
    print(job["ClusterId"],"\t", \
          statuses[job["JobStatus"]],"\t", \
          job["Cmd"],"\t", \
          job.get("DockerImage", "none"),"\t", \
	  deltatime(job["EnteredCurrentStatus"]))

