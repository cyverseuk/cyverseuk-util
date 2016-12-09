from __future__ import print_function
import htcondor
import time
import subprocess
import socket
import pickle
import struct

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


def analyzeSlots( coll , stats ):

    slots = coll.query()
    slotindex = 0
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


    totalcpus = 0
    totalmem = 0

    for i in range (0, len(out)):
        if out[i][0] is 0:
            simplename = out[i][1].replace("slot1@","")
 
            stats["condor." + simplename + ".cpus"] = out[i][3]
            stats["condor." + simplename + ".mem"] = out[i][5]

            totalcpus += out[i][3]
            totalmem += out[i][5]
    
    stats["condor.total.cpus"] = totalcpus
    stats["condor.total.mem"] = totalmem

def analyzeQueue( schedd , stats ):

    jobs = schedd.query()

    #statuses = {
    #    1: 'Idle',
    #    2: 'Running',
    #    3: 'Removed',
    #    4: 'Completed',
    #    5: 'Held',
    #    6: 'Submission Error'
    #}

    jobsheld = 0
    jobsidle = 0
    jobsrunning = 0

    for job in jobs:
        if int(job["JobStatus"]) is 1:
            jobsidle += 1
        if int(job["JobStatus"]) is 2:
            jobsrunning += 1
        if int(job["JobStatus"]) is 5:
            jobsheld += 1

    stats["condor.total.jobsrunning"] = jobsrunning
    stats["condor.total.jobsidle"] = jobsidle
    stats["condor.total.jobsheld"] = jobsheld

def pingGraphite(stats, sock):
    print("found the following stats:")
    for key in stats.keys():
        print(key + ": " + str(stats[key]))

    #for key in stats.keys():
    #    cmd = "echo -n \""+ key + ":" + str(stats[key]) + "|c\" | nc -q0 -u -w1 localhost 8125"
    #    #print("running command: " + cmd)
    #    subprocess.call(cmd, shell=True)

    # use pickle for message sending
    tuples = ([])
    lines = []

    now = int(time.time())

    for key in stats.keys():
        tuples.append((key, (now,stats[key])))
        lines.append(key + " %s %d" % (now,stats[key]))

    message = '\n'.join(lines) + '\n' #all lines must end in a newline
    print("sending message")
    print('-' * 80)
    print(message)

    package = pickle.dumps(tuples, 1)
    size = struct.pack('!L', len(package))

    # send it away, ahoy!
    sock.sendall(size)
    sock.sendall(package)

def main():
    
    stats = {}

    coll = htcondor.Collector("10.0.72.94:4080?addrs=10.0.72.94-4080&noUDP&sock=collector")
    analyzeSlots(coll, stats)

    schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd)
    schedd = htcondor.Schedd(schedd_ad)
    analyzeQueue(schedd, stats)

    sock = socket.socket()
    try:
        sock.connect( ("localhost", 2004) )
    except socket.error:
        raise SystemExit("couldn't open connection to graphite")

    try:
        pingGraphite(stats, sock)
    except KeyboardInterrupt:
        sys.stderr.write("\nExiting on CTRL-c\n")
        sys.exit(0)

main()
