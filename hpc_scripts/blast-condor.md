# blast-condor
A perl script to split a BLAST search into multiple jobs for HTCondor

#Synopsis
       blast-condor.pl -b blastcmd -q in.fa -d db.blastdb [-j jobs]

#Description
       --blastcommand, -b  Full path to the blast program to run (blastn, blastx, etc.)

       --query, -q         FASTA file with query sequences

       --database, -d      BLAST database file

       --jobs, -j          Number of jobs to generate

       --transfer-off, -t  Don't use Condor's file transfer mechanism

       --arguments, -a     Additional blast command line parameters

       --man, -m           Show this help

#Author
       Erik van den Bergh

