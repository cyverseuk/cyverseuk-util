use warnings;
use strict;

my $condor_status = `condor_status -autoformat Name State LoadAvg Memory`;
open my $cf, '<', \$condor_status or die $!;

my %claimed; 
my %free; 
my %mem;
my %load;

while (<$cf>) {
  chomp;
  (my $slotfull, my $claimed, my $load, my $mem) = split / /;
  (my $slot, my $host) = split(/@/,$slotfull);

  $load{$host} += $load if exists $load{$host};
  $load{$host} = $load if !exists $load{$host};

  $mem{$host} += $mem if exists $mem{$host};
  $mem{$host} = $mem if !exists $mem{$host};

  if ($claimed eq "Claimed") { 
    if(exists $claimed{$host}) { 
      $claimed{$host}++; 
    } else { 
      $claimed{$host} = 1; 
      $free{$host} = 0 if !exists $free{$host};
    } 
  } else { 
    if (exists $free{$host}) {
      $free{$host}++;
    } else {
      $free{$host}=  1;
      $claimed{$host} = 0 if !exists $claimed{$host};
    }
  }
}

print "host\t\t\tslots\tload\tmem\n";
for my $host (sort(keys %claimed)) {
  my $total = $claimed{$host} + $free{$host};
  print "$host:\t$claimed{$host} / $total\t$load{$host}\t$mem{$host}\n";
}
