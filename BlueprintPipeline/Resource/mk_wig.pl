#!/usr/bin/perl
use strict;
use warnings;
my $chr="";
my $lchr="";
my $x=0;
my ($n,$m1,$s1);
my $date=shift or die;
my $sm=shift || die;
open OF1,">$sm.CPG_methylation_calls.bs_call.$date.wig" or die "$!";
open OF2,">$sm.CPG_methylation_calls.bs_cov.$date.wig" or die "$!";
open FILE,"zcat $sm\_cpg.txt.gz |" || die "$!";
while(<FILE>) {
	 chomp;
	 my @fd=split "\t";
		if($fd[3] eq "CG" && $fd[4]>=2 && $fd[5] ne "-") {
				$chr=$fd[0];
				if($chr ne $lchr) {
						print OF1 "variableStep\tchrom=$chr\tspan=2\n";
						print OF2 "variableStep\tchrom=$chr\tspan=2\n";
						print "Sample $sm: chrom $chr\n";
						$lchr=$chr;
				}
				my $cov=$fd[7]+$fd[8];
				print OF1 "$fd[1]\t$fd[5]\n";
				print OF2 "$fd[1]\t$cov\n";
		}
}
close FILE;
close OF1;
close OF2;
