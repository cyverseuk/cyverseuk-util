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

--transfer-off, -t	Don't use Condor's file transfer mechanism

--arguments, -a  	Additional blast command line parameters

--man, -m		Show this help

=head1 AUTHOR

Erik van den Bergh

=cut


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
           "transfer-off"   => \$notransfer,
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
open JF, ">$qf.job$jobi" or die $!;

my $cc = 0;

sub gen_submit() {
  open SF, ">blast.htc" or die $!;

  print SF "Executable = $blastcmd\n";
  print SF "Log = $qf.blast.log\n";
  print SF "Output = $qf.blast.out\n";
  print SF "Arguments = -query $qf.job\$(Process) -db $db ".$blastargs."\n";

  if (!$notransfer) {
    print SF "should_transfer_files = YES\n";
    print SF "when_to_transfer_output = ON_EXIT\n";
  }

  print SF "Queue $jobi";

  close SF;
}

sub process_record($) {
  if ($cc > $chunksize) {
    close JF;

    $jobi++;
    my $jfp = "$qf.job$jobi";
    open JF, ">$jfp" or die $!;

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

gen_submit();

print STDERR "Split query file into $jobi files.\n";
print STDERR "Run \"condor_submit blast.htc\" to run your BLAST. ";
print STDERR "Thank you for using blast-condor, have a great day.\n";
