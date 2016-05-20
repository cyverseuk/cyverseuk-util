__author__ = 'Ryan Joynson'

import os
import argparse
import shutil
import glob
import sys
parser = argparse.ArgumentParser(description="Process Tuxedo suite command input")
parser.add_argument("-indx", action="store")
parser.add_argument("-indpre", action="store")
parser.add_argument("-input1", action="store", nargs='*')
parser.add_argument("-input2", action="store", nargs='*')
parser.add_argument("-input3", action="store", nargs='*')
parser.add_argument("-input4", action="store", nargs='*')
parser.add_argument("-input5", action="store", nargs='*')
parser.add_argument("-input6", action="store", nargs='*')
parser.add_argument("-input7", action="store", nargs='*')
parser.add_argument("-input8", action="store", nargs='*')
parser.add_argument("-gtf", action ="store")
parser.add_argument("-proc", action ="store")
parser.add_argument("-lab1", action ="store")
parser.add_argument("-lab2", action ="store")
parser.add_argument("-lab3", action ="store")
parser.add_argument("-lab4", action ="store")
#Tophat2 specific options
parser.add_argument("-a", action ="store", help="Tophat -r mate inner distance <int>")
parser.add_argument("-b", action ="store", help="Tophat --mate-std-dev std dev of inner mate distance <int>")
parser.add_argument("-c", action ="store_true", help="Tophat --no-discordant or report concordant mapping")
parser.add_argument("-d", action ="store_true", help="Tophat --no-mixed only report alignments if both reads map")
parser.add_argument("-e", action ="store", help="Tophat --library-type e.g. fr-firststrand (see manual)")
parser.add_argument("-f", action ="store", help="Tophat/Bowtie2: --very-fast --fast --sensitive  ")
#create drop down option box in DE for --very fast --fast etc. The make DE input -f 1 or -f 2 or -f 3 or -f 4 then link --fast etc. to a number later in tophat part if args.a == 1 append... elif == 2 append... etc.
parser.add_argument("-g", action ="store_true", help="Tophat phred64/solexa64 quality scores (deafault is phred33)>")
parser.add_argument("-i", action ="store", help="Tophat -a min anchor length <int>")
parser.add_argument("-j", action ="store", help="Tophat -g max multihits <int>")
parser.add_argument("-k", action ="store", help="Tophat -i min-intron-length <int>")
parser.add_argument("-l", action ="store", help="Tophat -I max-intron-length <int>")
parser.add_argument("-m", action ="store", help="Tophat --segment-length reads cut up into segments longer than this number <int>")
#Cufflinks specific options
parser.add_argument("-n", action ="store_true", help="Cufflinks -g GTF-guide use GTF to guide assembly")
parser.add_argument("-o", action ="store", help="Cufflinks -M mask file containing transcripts to be ignored")
parser.add_argument("-p", action ="store_true", help="Cufflinks -u use rescue method for multi-reads")
parser.add_argument("-Q", action ="store", help="Cufflinks --max-mle-iterations maximum iterations allowed for MLE calculation")
parser.add_argument("-q", action ="store", help="Cufflinks -L transcript prefix id default is CUFF")
parser.add_argument("-s", action ="store", help="Cufflinks -F min isoform fraction, suppress transcrips below this integer")
parser.add_argument("-t", action ="store", help="Cufflinks -j suppress intra-intronic transcripts below this ineger")
parser.add_argument("-u", action ="store", help="Cufflinks -I maximum intron length (ignore alignments with gaps bigger) ")
parser.add_argument("-v", action ="store", help="Cufflinks -a alpha for junction binomial test filter")
parser.add_argument("-w", action ="store", help="Cufflinks -A small anchor fraction (% of read overhang taken as suspiciously small)")
parser.add_argument("-x", action ="store", help="Cufflinks --min-frags-per-transfrag,minimum number of fragments needed for new transfrags")
parser.add_argument("-y", action ="store", help="Cufflinks --overhang-tolerance, number of terminal exon bp to tolerate in introns ")
parser.add_argument("-z", action ="store", help="Cufflinks --min-intron-length, minimum intron size allowed in genome")
parser.add_argument("-A", action ="store", help="Cufflinks --trim-3-avgcov-thresh, minimum avg coverage required to attempt 3' trimming ")
parser.add_argument("-B", action ="store", help="Cufflinks --trim-3-dropoff-frac, fraction of avg coverage below which to trim 3' end")
parser.add_argument("-C", action ="store", help="Cufflinks --overlap-radius, maximum gap size to fill between transfrags (in bp)")
#Cuffdiff options
parser.add_argument("-D", action ="store_true", help="Cuffdiff -b fragment bias correction using ref sequence")
parser.add_argument("-E", action ="store", help="Cuffdiff -M mask file with transcripts to ignore")
parser.add_argument("-F", action ="store_true", help="Cuffdiff -u use multi read hit rescue method")
parser.add_argument("-G", action ="store", help="Cuffdiff -c minimum number of alignments in a locus for testing")
parser.add_argument("-H", action ="store", help="Cuffdiff --FDR false discovery rate used in testing")
parser.add_argument("-I", action ="store_true", help="Cuffdiff switches from only ref RNA to all hits for normalization") #in DE just put no option/argument for only transcripts in reference and -I for all transcripts for normalization


args = parser.parse_args()

# ----------------------------------------------BOWTIE2-BUILD----------------------------------------------------------

bowtie2build = "bowtie2-build"

build_command = [bowtie2build]

#build bowtie2-build command
if args.indx and args.indpre:
	build_command.extend([args.indx, args.indpre])
else: pass

final_bowtie2_build = " ".join(build_command)

os.system(final_bowtie2_build)

# ---------------------------------------------TOPHAT2 analysis ------------------------------------------------------

tophat2 = "tophat2"
#add user options to command
tophat2_command = [tophat2, "-p", args.proc]
if args.gtf: tophat2_command.extend(["-G", args.gtf])
if args.a: tophat2_command.extend(["-r", args.a])
if args.b: tophat2_command.extend(["--mate-std-dev", args.b])
if args.c: tophat2_command.extend(["--no-discordant"])
if args.d: tophat2_command.extend(["--no-mixed"])
if args.e: tophat2_command.extend(["--library-type", args.e]) #check how best can be done when DE is back up
if args.f == "1": tophat2_command.append("--b2-very-fast")
elif args.f == "2": tophat2_command.append("--b2-fast")
elif args.f == "3": tophat2_command.append("--b2-sensitive")
elif args.f == "4": tophat2_command.append("--b2-very-sensitive")
if args.g: tophat2_command.extend(["--phred64-quals"])
if args.i: tophat2_command.extend(["-a", args.i])
if args.j: tophat2_command.extend(["-g", args.j])
if args.k: tophat2_command.extend(["-i", args.k])
if args.l: tophat2_command.extend(["-I", args.l])
if args.m: tophat2_command.extend(["--segment-length", args.m ])
con_1_folder = 1
#loop to iterate over all input pairs for condition 1 - TopHat2
if args.input1 and args.input2:
    for x, y in list(zip(args.input1, args.input2)):
        output_directory1 = "-o ./output/tophat2_condition_1_rep_%d" % output_dir,con_1_folder
        tophat2_command.extend([output_directory1, args.indpre, x, y])
        final_command = " ".join(tophat2_command)
        print("\n",final_command)
        os.system(final_command)
        if not os.path.exists("./output/condition1_accepted_hits"): os.mkdir("./output/condition1_accepted_hits", % output_dir)
        shutil.copy("./output/tophat2_condition_1_rep_%d/accepted_hits.bam" % output_dir,con_1_folder, "./output/condition1_accepted_hits/accepted_hits_condition1_rep_%d.bam" % con_1_folder)
        del tophat2_command[-4:]
        con_1_folder += 1
else: pass
#loop to iterate over all input pairs for condition 2 - TopHat2
con_2_folder = 1
if args.input3 and args.input4:
    for x, y in list(zip(args.input3, args.input4)):
        output_directory2 = "-o ./output/tophat2_condition_2_rep_%d" % con_2_folder
        tophat2_command.extend([output_directory2, args.indpre, x, y])
        final_command = " ".join(tophat2_command)
        print("\n",final_command)
        os.system(final_command)
        if not os.path.exists("./output/condition2_accepted_hits"): os.mkdir("./output/condition2_accepted_hits")
        shutil.copy("./output/tophat2_condition_2_rep_%d/accepted_hits.bam" % con_2_folder, "./output/condition2_accepted_hits/accepted_hits_condition2_rep_%d.bam" % con_2_folder)
        del tophat2_command[-4:]
        con_2_folder += 1
else: pass

con_3_folder = 1
if args.input5 and args.input6:
    for x, y in list(zip(args.input5, args.input6)):
        output_directory3 = "-o ./output/tophat2_condition_3_rep_%d" % con_3_folder
        tophat2_command.extend([output_directory3, args.indpre, x, y])
        final_command = " ".join(tophat2_command)
        print("\n",final_command)
        os.system(final_command)
        if not os.path.exists("./output/condition3_accepted_hits"): os.mkdir("./output/condition3_accepted_hits")
        shutil.copy("./output/tophat2_condition_3_rep_%d/accepted_hits.bam" % con_3_folder, "./output/condition3_accepted_hits/accepted_hits_condition3_rep_%d.bam" % con_3_folder)
        del tophat2_command[-4:]
        con_3_folder += 1
else: pass

con_4_folder = 1
if args.input7 and args.input8:
    for x, y in list(zip(args.input7, args.input8)):
        output_directory4 = "-o ./output/tophat2_condition_4_rep_%d" % con_4_folder
        tophat2_command.extend([output_directory4, args.indpre, x, y])
        final_command = " ".join(tophat2_command)
        print("\n",final_command)
        os.system(final_command)
        if not os.path.exists("./output/condition4_accepted_hits"): os.mkdir("./output/condition4_accepted_hits")
        shutil.copy("./output/tophat2_condition_4_rep_%d/accepted_hits.bam" % con_4_folder, "./output/condition4_accepted_hits/accepted_hits_condition4_rep_%d.bam" % con_4_folder)
        del tophat2_command[-4:]
        con_4_folder += 1
else: pass

# ------------------------------------------ Cufflinks Analysis -------------------------------------------------------
#Binary location
cufflinks = "cufflinks"
#Start of cufflinks command
cufflinks_command = [cufflinks, "-p", args.proc, "--library-type", args.e, "-L", args.q, "-F", args.s, "-j", args.t, "-I", args.u, "-a", args.v, "-A", args.w, "--min-frags-per-transfrag", args.x, "--overhang-tolerance", args.y, "--min-intron-length", args.z, "--trim-3-avgcov-thresh", args.A, "--trim-3-dropoff-frac", args.B, "--overlap-radius", args.C]
#add user options to command
if args.n: cufflinks_command.extend(["-g", args.gtf])
if args.o: cufflinks_command.extend(["-M", args.o])
if args.p: cufflinks_command.append("-u")
if args.Q: cufflinks_command.extend(["--max-mle-iterations", args.Q])

#Condition 1 Cufflinks loop
bam_list = sorted(glob.glob("tophat2_condition_1*/accepted_hits.bam"))
if not os.path.exists("./output/assembled_transcripts"): os.mkdir("./output/assembled_transcripts")
print(bam_list)
cuff_con1_folder = 1
for bam in list(zip(bam_list)):
    cuff_out = "-o ./output/cufflinks_condition_1_rep_%d" % cuff_con1_folder
    cufflinks_command.append(cuff_out)
    cufflinks_command.extend(bam)
    final_cufflinks_command = " ".join(cufflinks_command)
    print(final_cufflinks_command)
    os.system(final_cufflinks_command)
    shutil.copy("./output/cufflinks_condition_1_rep_%d/transcripts.gtf" % cuff_con1_folder, "./output/assembled_transcripts/transcripts_condition1_rep_%d.gtf" % cuff_con1_folder)
    del cufflinks_command[-2:]
    cuff_con1_folder += 1
#Condition 2 Cufflinks loop
bam_list2 = sorted(glob.glob("tophat2_condition_2*/accepted_hits.bam"))
print(bam_list2)
cuff_con2_folder = 1
for bam in list(zip(bam_list2)):
    cuff_out = "-o ./output/cufflinks_condition_2_rep_%d" % cuff_con2_folder
    cufflinks_command.append(cuff_out)
    cufflinks_command.extend(bam)
    final_cufflinks_command = " ".join(cufflinks_command)
    os.system(final_cufflinks_command)
    shutil.copy("./output/cufflinks_condition_2_rep_%d/transcripts.gtf" % cuff_con2_folder, "./output/assembled_transcripts/transcripts_condition2_rep_%d.gtf" % cuff_con2_folder)
    del cufflinks_command[-2:]
    cuff_con2_folder += 1
#Condition 3 Cufflinks loop
bam_list3 = sorted(glob.glob("tophat2_condition_3*/accepted_hits.bam"))
print(bam_list3)
cuff_con3_folder = 1
for bam in list(zip(bam_list3)):
    cuff_out = "-o ./output/cufflinks_condition_3_rep_%d" % cuff_con3_folder
    cufflinks_command.append(cuff_out)
    cufflinks_command.extend(bam)
    final_cufflinks_command = " ".join(cufflinks_command)
    print(final_cufflinks_command)
    os.system(final_cufflinks_command)
    shutil.copy("./output/cufflinks_condition_3_rep_%d/transcripts.gtf" % cuff_con3_folder, "./output/assembled_transcripts/transcripts_condition3_rep_%d.gtf" % cuff_con3_folder)
    del cufflinks_command[-2:]
    cuff_con3_folder += 1
#Condition 4 Cufflinks loop
bam_list4 = sorted(glob.glob("tophat2_condition_4*/accepted_hits.bam"))
print(bam_list4)
cuff_con4_folder = 1
for bam in list(zip(bam_list4)):
    cuff_out = "-o ./output/cufflinks_condition_4_rep_%d" % cuff_con4_folder
    cufflinks_command.append(cuff_out)
    cufflinks_command.extend(bam)
    final_cufflinks_command = " ".join(cufflinks_command)
    print(final_cufflinks_command)
    os.system(final_cufflinks_command)
    shutil.copy("./output/cufflinks_condition_4_rep_%d/transcripts.gtf" % cuff_con4_folder, "./output/assembled_transcripts/transcripts_condition4_rep_%d.gtf" % cuff_con4_folder)
    del cufflinks_command[-2:]
    cuff_con4_folder += 1

#-------------------------------------------- Cuffmerge Analysis ------------------------------------------------------

cuffmerge = "cuffmerge"
cuffmerge_command = [cuffmerge, "-p", args.proc, "-o cuffmerge_gtf"]
#make list of gtfs
the_list = glob.glob("./output/assembled_transcripts/*.gtf")
print(the_list)
#create txt input file containing gtfs line by line
f =open("file.txt", "w")
for ele in the_list:
    f.write(ele+"\n")
f.close()
# create and run cuffmerge command
if args.gtf: cuffmerge_command.extend(["-g", args.gtf])
cuffmerge_command.extend(["-s", args.indx, "file.txt"])
final_cuffmerge_command = " ".join(cuffmerge_command)
print(final_cuffmerge_command)
os.system(final_cuffmerge_command)

#-------------------------------------------- Cuffdiff Analysis ------------------------------------------------------

cuffdiff =  ("cuffdiff")
#make list of condition labels from inputs
labels = []
if args.input1 and args.input2: labels.append(args.lab1)
if args.input3 and args.input4: labels.append(args.lab2)
if args.input5 and args.input6: labels.append(args.lab3)
if args.input7 and args.input8: labels.append(args.lab4)
labels2 = ",".join(labels)
print(labels2)
cuffdiff_command = [cuffdiff, "-p", args.proc, "-L", labels2, "--library-type", args.e, "-c", args.G, "--FDR", args.H, "-o cuff_diff_out", "./output/cuffmerge_gtf/merged.gtf"]
if args.D: cuffdiff_command.insert(-2, "-b %s" %args.indx)
if args.E: cuffdiff_command.insert(-2, "-M %s" %args.E)
if args.F: cuffdiff_command.insert(-2, "-u")
if args.I: cuffdiff_command.insert(-2, "--total-hits-norm")
#make list of folders containing assembled transcripts
dir_list = glob.glob("./output/condition?_accepted_hits")
print(dir_list)
dir_list2 = sorted(dir_list)
for bam in dir_list2:
    files = sorted(glob.glob("%s/*.bam" %bam))
    print(files)
    file2 = ",".join(files)
    cuffdiff_command.append(file2)

cuffdiff_final = " ".join(cuffdiff_command)
print(cuffdiff_final)

os.system(cuffdiff_final)

#-------------------------------------------- CummeRbund ------------------------------------------------------

if not os.path.exists("./output/r_plots"): os.mkdir("./output/r_plots")
plot_script = "Rscript /cummerbund_plot_scripts.r"

os.system(plot_script)

#-------------------------------------------- Cleaning ------------------------------------------------------

os.system("rm -r ./output/assembled_transcripts ./output/condition* ./output/file.txt")
os.system("mkdir -p ./output/index_files/; mv %s* ./output/index_files" %args.indpre)
