# blast-condor
A perl script to split a BLAST search into multiple jobs

#SYNOPSIS
       blast-condor.pl -b blastcmd -q in.fa -d db.blastdb [-n num_jobs]

#DESCRIPTION
       --blastcommand, -b  Full path to the blast program to run (blastn, blastx, etc.)

       --query, -q         FASTA file with query sequences

       --database, -d      BLAST database file

       --num-jobs, -n      Number of jobs to generate

       --transfer-off, -t  Don't use Condor's file transfer mechanism

       --arguments, -a     Additional blast command line parameters

       --man, -m      Show this help

#AUTHOR
       Erik van den Bergh

