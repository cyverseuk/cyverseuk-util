#TODO separate output files, right now the single one is overwrtten

use warnings;
use strict;

use Pod::Usage;
use Getopt::Long;

=head1 SYNOPSIS

blast-condor.pl -b blastcmd -q in.fa -d db.blastdb [-j jobs]

=head1 DESCRIPTION

--blastcommand, -b	Full path to the blast program to run (blastn, blastx, etc.)

--query, -q		FASTA file with query sequences

--database, -d		BLAST database file

--jobs, -j		Number of jobs to generate

--arguments, -a  	Additional blast command line parameters

--man, -m		Show this help

=head1 AUTHOR

Erik van den Bergh

=cut

#lets not pollute our local dir shall we?
`mkdir -p slurmout`;

chomp(my $wd = `pwd`);

my $blastcmd = "";

my $qf = "";
my $db = "";

my $jobs = "4";

my $notransfer = 0;

my $blastargs = "";

(my $man, my $help);

GetOptions("blastcommand=s" => \$blastcmd,
	   "query=s"	    => \$qf,
	   "database=s"	    => \$db,
	   "jobs=i"	    => \$jobs,
           "arguments=s"    => \$blastargs,
	   "man"	    => \$man,
	   "help"	    => \$help)
or pod2usage(1);

if ($help) { pod2usage(1); }
if ($man)  { pod2usage(-verbose=>2); }

if ($blastcmd eq "" || $qf eq "" || $db eq "") {
  pod2usage(1);
}

open QF, $qf or die pod2usage(1);

my $wc = `wc -c $qf`;
(my $qfc, my $temp) = split(/ /,$wc);

my $chunksize = $qfc / $jobs;

my $id = "";
my $seq = "";

my $jobi = 0;
open JF, ">slurmout/$qf.job$jobi" or die $!;

my $cc = 0;

sub gen_batch() {
  open BF, ">$qf.batch" or die $!;
  
  print BF "#!/bin/sh\n";
  print BF "#SBATCH --input $wd"."/slurmout/$qf.job%j --output $wd"."/slurmout/$qf.out.job%j -n$jobs\n";
  print BF "srun $blastcmd -query - -db $wd"."/$db -outfmt 6 $blastargs\n";

  close BF;
}

sub process_record($) {
  if ($cc > $chunksize) {
    close JF;

    $jobi++;
    my $jfp = "$qf.job$jobi";
    open JF, ">slurmout/$jfp" or die $!;

    $cc = 0;
  }

  print JF "$id\n$seq\n";
  $id = shift;
  $seq = "";
  $cc += length($id);
}

while (<QF>) {
  chomp;
  if (m/>/) { 
    process_record($_) 
  } else {
    $seq .= $_;
    $cc += length($_);
  } 
}

process_record("");

gen_batch();

my $files = $jobi + 1;
print STDERR "Split query file into $files files.\n";
print STDERR "Run \"sbatch $qf.batch\" to run your BLAST. ";
print STDERR "Thank you for using blast-slurm, have a great day.\n";
